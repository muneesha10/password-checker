# Password Strength Checker

A beginner-friendly Streamlit project that evaluates password characteristics locally. It checks length, character variety, common passwords, repeated characters, and simple ascending or descending sequences. The app provides a score from 0 to 100, a strength level, a checklist, and suggestions.

## Features

- Password input with a show/hide toggle and reset button.
- Local checks using Python and regular expressions. No password is stored in a file, logged, or sent to an external service.
- A 0-100 heuristic score with five strength levels and a colored progress bar.
- Checklist and suggestions for improving the password.
- Responsive dark interface with blue and green accents.
- A privacy note explaining the tool's limitations.

The score is an educational estimate, not a password-cracking test or a guarantee of security. This project does not check breached-password databases. Use a unique password for each account and consider using a reputable password manager.

For local-only processing, run the app on your own machine at `localhost`. Streamlit Community Cloud runs the app on a remote server, so browser input is transmitted to that server for analysis. Use only fabricated sample passwords in any hosted deployment, never real account credentials.

## Requirements

- Python 3.9 or newer
- Visual Studio Code
- A terminal (the integrated VS Code terminal works)

## Create the project in VS Code

1. Create a folder named `password-checker` and open it in VS Code (`File > Open Folder...`).
2. Create `app.py`, `requirements.txt`, `README.md`, and `.gitignore` in the project folder, then add the contents provided for each file.
3. Open the integrated terminal with `Terminal > New Terminal`.

## Install and run

In the VS Code terminal, create and activate a virtual environment, then install dependencies:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks environment activation, use `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` and run Streamlit with `.\.venv\Scripts\python.exe -m streamlit run app.py` instead. On macOS or Linux, activate with `source .venv/bin/activate`.

Start the application:

```powershell
streamlit run app.py
```

Streamlit opens the app in your browser, usually at [http://localhost:8501](http://localhost:8501). If it does not open automatically, enter that address in a browser.

## Try sample passwords

Use examples only; do not enter a real password that you currently use.

- `password123` demonstrates common-password detection.
- `abcdef12345!` demonstrates ascending letter and number sequences.
- `CorrectHorse9!Battery` demonstrates a longer password with varied character types.

Use **Show password** to toggle visibility and **Reset** to clear the input. Results update as you enter a value.

## Upload to GitHub

1. Create a new empty repository on GitHub. Do not include a generated README if you already have this project README.
2. In the project terminal, initialize Git and commit the project:

```powershell
git init
git add app.py requirements.txt README.md .gitignore
git commit -m "Add password strength checker"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the remote URL with your repository URL. Do not commit real passwords, secrets, or `.streamlit/secrets.toml`.

## Deploy with Streamlit Community Cloud

1. Push the project to GitHub and sign in at [share.streamlit.io](https://share.streamlit.io/) with an account that can access the repository.
2. Select **Create app**, choose the repository, branch (`main`), and main file path (`app.py`).
3. Select **Deploy**. Community Cloud installs dependencies from `requirements.txt` and builds the app.
4. When deployment succeeds, copy the app URL shown by Community Cloud to share it.

The app does not use secrets or call external password services. Community Cloud receives entered values at its remote app server for analysis; use fabricated samples there, not real account credentials.