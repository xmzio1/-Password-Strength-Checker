# 🔐 Password Strength Checker

## 📌 Overview
A simple **Python CLI tool** to evaluate the strength of passwords and provide a detailed security report.  
The project aims to help users understand whether their passwords are weak, predictable, or exposed to common attack patterns.

## ✨ Features
- Calculates password strength using **entropy (log2)**.  
- Checks for:
  - Lowercase letters (a-z)  
  - Uppercase letters (A-Z)  
  - Numbers (0-9)  
  - Special symbols (!@#...)  
- Detects repeated characters and sequences (e.g., `aaa111`, `abcabc`).  
- Identifies common keyboard patterns (`qwerty`, `asdf`, `12345`, etc.).  
- Compares against a **list of 500 common passwords** (`common_passwords_500.txt`).  
- Provides actionable suggestions to improve password security.

## 🛠️ Technologies
- **Python 3**  
- **Regex** for pattern matching  
- **Math / log2** for entropy calculation  
- **Argparse** for command-line usage  
- External **dictionary file** for common passwords

## 🚀 Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/username/password-checker.git
   cd password-checker
## 📊 Example Output
=== Password Strength Report ===
Password: MyPass123!
Length: 10  |  Estimated entropy: 59.52 bits
Overall rating: Strong  |  Score metric: 3

Issues found:
 - Contains a known keyboard pattern (e.g., qwerty, 12345).

Suggestions to improve your password:
 - Make the password 12+ characters for better security.
 - Use a passphrase instead of a short word.
 - Mix uppercase, lowercase, numbers, and symbols.
 - Avoid common words or keyboard sequences.
 - Use a password manager to generate and store unique strong passwords.
=============================

