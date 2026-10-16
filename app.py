import re

import streamlit as st


COMMON_PASSWORDS = {
    "123456",
    "123456789",
    "abc123",
    "admin",
    "dragon",
    "iloveyou",
    "letmein",
    "monkey",
    "password",
    "password1",
    "password123",
    "qwerty",
    "welcome",
}

REPEATED_CHARACTER_PATTERN = re.compile(r"(.)\1{2,}")


def contains_simple_sequence(password: str, minimum_length: int = 4) -> bool:
    """Return whether a password contains a run of adjacent letters or digits."""
    normalized_password = password.lower()

    for start in range(len(normalized_password) - minimum_length + 1):
        sequence = normalized_password[start : start + minimum_length]
        if not sequence.isalnum():
            continue

        differences = [
            ord(next_character) - ord(current_character)
            for current_character, next_character in zip(sequence, sequence[1:])
        ]
        if all(difference == 1 for difference in differences) or all(
            difference == -1 for difference in differences
        ):
            return True

    return False


def analyze_password(password: str) -> dict[str, object]:
    """Evaluate password characteristics without saving or transmitting the input."""
    checks = {
        "At least 12 characters": len(password) >= 12,
        "Contains an uppercase letter": bool(re.search(r"[A-Z]", password)),
        "Contains a lowercase letter": bool(re.search(r"[a-z]", password)),
        "Contains a number": bool(re.search(r"\d", password)),
        "Contains a special character": bool(re.search(r"[^A-Za-z0-9]", password)),
        "Not a common, easily guessed password": password.lower() not in COMMON_PASSWORDS,
        "No character repeated three or more times in a row": not bool(
            REPEATED_CHARACTER_PATTERN.search(password)
        ),
        "No 4-character ascending or descending sequence": not contains_simple_sequence(
            password
        ),
    }

    # Length is weighted separately so a short password cannot earn a top score
    # just by mixing character types.
    if len(password) < 8:
        length_points = 0
        score_cap = 39
    elif len(password) < 12:
        length_points = 12
        score_cap = 69
    elif len(password) < 16:
        length_points = 24
        score_cap = 100
    else:
        length_points = 32
        score_cap = 100

    score = length_points
    score += sum(
        10
        for label in (
            "Contains an uppercase letter",
            "Contains a lowercase letter",
            "Contains a number",
            "Contains a special character",
        )
        if checks[label]
    )
    score += 15 if checks["Not a common, easily guessed password"] else 0
    score += 7 if checks["No character repeated three or more times in a row"] else 0
    score += 6 if checks["No 4-character ascending or descending sequence"] else 0
    score = min(score, score_cap)
    if not checks["Not a common, easily guessed password"]:
        score = min(score, 19)
    if not checks["No 4-character ascending or descending sequence"]:
        score = min(score, 59)

    if score < 20:
        level = "Very Weak"
    elif score < 40:
        level = "Weak"
    elif score < 60:
        level = "Moderate"
    elif score < 80:
        level = "Strong"
    else:
        level = "Very Strong"

    suggestions = []
    if len(password) < 12:
        suggestions.append("Use at least 12 characters; a longer passphrase is even better.")
    if not checks["Contains an uppercase letter"]:
        suggestions.append("Add an uppercase letter.")
    if not checks["Contains a lowercase letter"]:
        suggestions.append("Add a lowercase letter.")
    if not checks["Contains a number"]:
        suggestions.append("Add a number.")
    if not checks["Contains a special character"]:
        suggestions.append("Add a special character, such as !, ?, or #.")
    if not checks["Not a common, easily guessed password"]:
        suggestions.append("Avoid common words, patterns, and predictable substitutions.")
    if not checks["No character repeated three or more times in a row"]:
        suggestions.append("Avoid repeating the same character several times in a row.")
    if not checks["No 4-character ascending or descending sequence"]:
        suggestions.append("Avoid sequences such as 1234 or abcd.")
    if not suggestions:
        suggestions.append("Good mix. Keep it unique to one account and store it in a password manager.")

    return {
        "score": score,
        "level": level,
        "checks": checks,
        "suggestions": suggestions,
    }


def reset_password() -> None:
    """Clear the input using a Streamlit button callback."""
    st.session_state["password_input"] = ""


def render_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            color-scheme: dark;
            --ink: #e9f2f7;
            --muted: #9bb0bf;
            --panel: #101d2a;
            --line: #263b4b;
            --blue: #42b7e9;
            --green: #47d7a0;
        }
        .stApp {
            background:
                radial-gradient(ellipse at 85% 5%, rgba(24, 103, 130, .22), transparent 35%),
                linear-gradient(145deg, #07111b 0%, #0b1722 55%, #0b1d24 100%);
            color: var(--ink);
        }
        header[data-testid="stHeader"], div[data-testid="stToolbar"] { background: #07111b; }
        .block-container { max-width: 940px; padding-top: 3rem; padding-bottom: 3rem; }
        h1, h2, h3, p, label { color: var(--ink); }
        h1 { letter-spacing: 0; font-size: 2.25rem; font-weight: 720; }
        .eyebrow {
            color: var(--green); font: 700 .78rem/1.4 sans-serif;
            letter-spacing: .12em; text-transform: uppercase; margin-bottom: .55rem;
        }
        .intro { color: var(--muted); max-width: 680px; font-size: 1rem; line-height: 1.65; }
        .result-panel {
            background: rgba(16, 29, 42, .88); border: 1px solid var(--line);
            border-radius: 8px; padding: 1.25rem 1.4rem; margin: .7rem 0 1rem;
        }
        .score-line { display: flex; align-items: baseline; justify-content: space-between; gap: 1rem; }
        .score-number { font-size: 2rem; font-weight: 750; }
        .score-level { font-weight: 700; }
        .meter { height: 10px; overflow: hidden; background: #243541; border-radius: 999px; margin-top: .65rem; }
        .meter-fill { height: 100%; border-radius: inherit; transition: width .25s ease; }
        .check-row { padding: .42rem 0; border-bottom: 1px solid rgba(155, 176, 191, .12); color: var(--muted); }
        .check-row:last-child { border-bottom: 0; }
        .privacy-note {
            color: var(--muted); font-size: .88rem; line-height: 1.6;
            border-left: 2px solid var(--blue); padding-left: .85rem;
        }
        div[data-testid="stTextInput"] input {
            background: #0d1a26; border-color: #385064; color: var(--ink);
        }
        div[data-testid="stTextInput"] button {
            background: #0d1a26; border-color: #385064; color: var(--muted);
        }
        div[data-testid="stCheckbox"] label { color: var(--muted); }
        div.stButton > button {
            border: 1px solid #3d6678; border-radius: 6px; color: var(--ink);
            background: #132635; min-height: 2.7rem;
        }
        div.stButton > button:hover { border-color: var(--green); color: var(--green); }
        @media (max-width: 640px) {
            .block-container { padding: 1.5rem 1rem 2rem; }
            h1 { font-size: 1.8rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(page_title="Password Strength Checker", page_icon="🔐", layout="centered")
    render_styles()

    st.markdown('<div class="eyebrow">Local security utility</div>', unsafe_allow_html=True)
    st.title("Password Strength Checker")
    st.markdown(
        '<p class="intro">Review a password against practical strength guidelines. '
        "The app does not query external password services.</p>",
        unsafe_allow_html=True,
    )

    show_password = st.checkbox("Show password", value=False, key="show_password")
    password = st.text_input(
        "Enter a password",
        type="default" if show_password else "password",
        key="password_input",
        autocomplete="new-password",
        help="The value is used only for this on-screen analysis.",
    )

    reset_column, _ = st.columns([1, 4])
    with reset_column:
        st.button("Reset", on_click=reset_password, use_container_width=True)

    if not password:
        st.info("Enter a password to see its checklist, score, and suggestions.")
    else:
        result = analyze_password(password)
        score = result["score"]
        level = result["level"]
        color = "#ed6a73" if score < 40 else "#f0b44d" if score < 60 else "#42b7e9" if score < 80 else "#47d7a0"

        st.markdown('<div class="result-panel">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="score-line"><span class="score-number">{score}<small> / 100</small></span>'
            f'<span class="score-level" style="color:{color}">{level}</span></div>'
            f'<div class="meter"><div class="meter-fill" style="width:{score}%;background:{color}"></div></div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        checklist_column, suggestions_column = st.columns(2, gap="large")
        with checklist_column:
            st.subheader("Requirements")
            for label, passed in result["checks"].items():
                icon = "✓" if passed else "·"
                color = "#47d7a0" if passed else "#9bb0bf"
                st.markdown(
                    f'<div class="check-row"><span style="color:{color};font-weight:700">{icon}</span>'
                    f"&nbsp; {label}</div>",
                    unsafe_allow_html=True,
                )
        with suggestions_column:
            st.subheader("Suggestions")
            for suggestion in result["suggestions"]:
                st.markdown(f"- {suggestion}")

    st.divider()
    st.markdown(
        '<p class="privacy-note"><strong>Privacy:</strong> The password is analyzed by the Streamlit server running this app; '
        "the app does not write it to a file or send it to third-party password services. Run on your own machine for local-only use. "
        "Do not enter real account passwords into a hosted deployment. This tool estimates strength and cannot guarantee security.</p>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()