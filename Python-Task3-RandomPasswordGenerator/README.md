\# Random Password Generator



\## Oasis Infobyte OIB-SIP — Python Programming Internship



\*\*Intern:\*\* Mohammed Amaan Ahmed

\*\*Track:\*\* Python Programming

\*\*Task:\*\* Task 3 — Random Password Generator

\*\*Tier:\*\* Advanced



\---



\## 1. Objective



Build a secure random password generator with configurable password length, character categories, password strength analysis, clipboard support, ambiguous-character exclusion, and temporary session history.



The application uses Python's `secrets` module for security-oriented password generation.



\---



\## 2. Features



\- Custom password length with minimum length of 8

\- Uppercase character selection

\- Lowercase character selection

\- Number selection

\- Symbol selection

\- Requires at least two character categories

\- Guarantees selected character categories are represented

\- Cryptographically secure generation using `secrets`

\- Password strength indicator

\- Estimated entropy calculation

\- Copy generated password to clipboard

\- Exclude ambiguous characters

\- Display the last five generated passwords for the current session

\- Session history is stored only in memory

\- No generated passwords are persisted to files

\- GUI validation and error handling

\- Automated unit tests



\---



\## 3. Technology Stack



\- Python 3.14

\- Tkinter

\- secrets

\- pyperclip

\- unittest



\---



\## 4. Project Structure



```text

Python-Task3-RandomPasswordGenerator/

│

├── README.md

├── requirements.txt

│

├── screenshots/

│   ├── 01-password-generator-main.png

│   ├── 02-minimum-length-8.png

│   ├── 03-category-validation-error.png

│   ├── 04-ambiguous-character-exclusion.png

│   ├── 05-session-history-five-items.png

│   └── 06-clean-startup.png

│

├── src/

│   ├── \_\_init\_\_.py

│   ├── generator.py

│   ├── strength.py

│   ├── clipboard.py

│   ├── session\_history.py

│   ├── gui.py

│   └── main.py

│

└── tests/

&#x20;   ├── \_\_init\_\_.py

&#x20;   ├── test\_generator.py

&#x20;   ├── test\_strength.py

&#x20;   ├── test\_clipboard.py

&#x20;   └── test\_session\_history.py

**Mohammed Amaan Ahmed**
