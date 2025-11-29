# 👁️ Argus

> *The All-Seeing Vulnerability Scanner*

**Argus** is a lightweight, automated security assessment tool designed to detect common web vulnerabilities with precision. Named after the hundred-eyed giant of Greek mythology, Argus keeps a vigilant watch over your web applications, identifying security flaws before they can be exploited.

## 🚀 Features

*   **SQL Injection (SQLi) Detection**: Automatically probes input fields with heuristic payloads to uncover potential database injection points.
*   **Cross-Site Scripting (XSS) Scanner**: Tests for Reflected XSS vulnerabilities by injecting and verifying payload execution in the DOM.
*   **Smart Navigation**: Powered by **Playwright**, Argus handles modern Single Page Applications (SPAs) and dynamic content with ease.
*   **Automated Reporting**: Generates detailed JSON reports of all findings for easy integration into CI/CD pipelines.
*   **Vulnerable Testbed**: Includes a purpose-built vulnerable Flask application for testing and educational demonstrations.

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/saadhtiwana/argus.git
    cd argus
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Playwright browsers**:
    ```bash
    playwright install
    ```

## 💻 Usage

### 1. Start the Vulnerable Application (Target)
Argus comes with a local test environment. Start the vulnerable app to see Argus in action:

```bash
python vulnerable_app.py
```
*The app will run at `http://127.0.0.1:5000`*

### 2. Run the Scanner
In a new terminal, launch Argus to scan the target:

```bash
python scanner.py
```

Argus will:
1.  Launch a browser instance.
2.  Navigate to the target URL.
3.  Identify interactive elements.
4.  Inject payloads for SQLi and XSS.
5.  Generate a `vulnerability_report.json` with the results.

## 📂 Project Structure

*   `scanner.py`: The core scanning engine using Playwright.
*   `vulnerable_app.py`: A Flask web app with intentional vulnerabilities (SQLi, XSS).
*   `vulnerable.db`: SQLite database for the test app.
*   `requirements.txt`: Python dependencies.

## ⚠️ Disclaimer

**Argus is for educational and authorized testing purposes only.**
Do not use this tool on systems you do not own or do not have explicit permission to test. The authors are not responsible for any misuse or damage caused by this tool.

---
*Built with Python, Playwright, and Vigilance.*
