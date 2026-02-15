# Auto Assignment Approval Script

This script automates the approval process for assignments on **Fasih SM BPS**. It logs in using your SSO credentials, processes assignment links from a CSV file, and approves them one by one.

## Features

- 🔐 **Secure Login**: Prompts for your SSO username and password at runtime (no hardcoded credentials).
- ⏳ **Smart Waits**: Automatically waits for buttons and elements to load before interacting, ensuring stability even with slow connections.
- 🔁 **Auto-Retry**: Automatically tracks failed assignments and attempts to process them again after the main batch is finished.
- 🚀 **Error Handling**: Skips problematic rows without crashing the entire script.

## Prerequisites

1.  **Python 3.x** installed.
2.  **Google Chrome** browser installed.
3.  Required Python packages:

    ```bash
    pip install selenium webdriver-manager
    ```

## Usage

1.  Ensure you have an `output.csv` file in the same directory. This file must contain a column named `Assignment Link`.
2.  Run the script:

    ```bash
    python approve_script.py
    ```

3.  Enter your SSO Username and Password when prompted.
4.  The browser will open and start processing the assignments.
5.  Sit back and relax! ☕

## How it Works

1.  **Login**: The script opens the login page and logs you in.
2.  **Read CSV**: It reads `output.csv` to get the list of assignments.
3.  **Process**: For each assignment:
    - Navigates to the details page.
    - Clicks **Review**.
    - Clicks **Approve**.
    - Confirms the action.
4.  **Retry**: If any assignments fail (e.g., page didn't load, button missing), they are added to a retry list and processed again at the end.

---

**Made with ❤️ by Albert Assidiq**
