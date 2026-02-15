import csv
import time
import os
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
# Try to import webdriver_manager, if not present, user needs to install it
try:
    from webdriver_manager.chrome import ChromeDriverManager
    HAS_WEBDRIVER_MANAGER = True
except ImportError:
    HAS_WEBDRIVER_MANAGER = False

# Configuration
BASE_URL = "https://fasih-sm.bps.go.id/survey-collection/assignment-detail/"
CSV_FILE = "output.csv"

def main():
    if not os.path.exists(CSV_FILE):
        print(f"Error: {CSV_FILE} not found.")
        return

    # 0. Get Credentials First
    print("="*50)
    print("masukkan akun sso bps nya")
    username = input("Enter your SSO Username: ")
    password = getpass.getpass("Enter your SSO Password: ")
    print("="*50)

    print("Initializing Browser...")
    
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Run in background if needed, but for visual confirmation keep it commented
    options.add_argument("--start-maximized")
    
    try:
        if HAS_WEBDRIVER_MANAGER:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        else:
            # Fallback to default path or require manual driver setup
            print("Note: 'webdriver-manager' not found. Trying default chromedriver...")
            driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"Error starting browser: {e}")
        print("Please ensure you have Chrome and chromedriver installed.")
        print("Recommended: pip install webdriver-manager selenium")
        return

    try:
        # 1. Automated Login Phase
        print("="*50)
        print("STEP 1: AUTOMATED LOGIN")
        print("Navigating to login page...")
        driver.get("https://fasih-sm.bps.go.id/oauth_login.html")
        
        wait = WebDriverWait(driver, 15)
        
        # Click "Login SSO BPS"
        print("   - Clicking 'Login SSO BPS'...")
        sso_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "login-button")))
        sso_btn.click()
        
        # Wait for SSO form
        print("   - Waiting for SSO form...")
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        
        # Enter credentials
        print("   - Entering credentials...")
        username_field.send_keys(username)
        
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        
        # Click Login
        login_btn = driver.find_element(By.ID, "kc-login")
        login_btn.click()

        print("   - Clicked 'Log In'")
        
        # Wait for login to complete (e.g., check for URL change or absence of login form)
        # We'll wait a bit for redirection
        time.sleep(5) 
        print("   - Login submitted. Waiting for redirection...")
        
        print("="*50)

        # 2. Read CSV Data
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        print(f"Found {len(rows)} data rows to process.")
        
        # 3. Process loop
        failed_rows = []

        def process_row(index, row_data, driver_instance, wait_instance):
            link_suffix = row_data.get("Assignment Link", "").strip()
            
            if not link_suffix:
                print(f"Row {index+1}: Skipped (No Assignment Link)")
                return True # "Success" in skipping

            full_url = BASE_URL + link_suffix
            print(f"[{index+1}/{len(rows)}] Visiting: {full_url}")
            
            driver_instance.get(full_url)
            
            try:
                # Wait for the page to load
                # A. Click "Review" button
                # Target: <a class="btn btn-primary float-right mr-2 ng-star-inserted">Review</a>
                print("   - Looking for 'Review' button...")
                review_btn = wait_instance.until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Review')]"))
                )
                review_btn.click()
                print("   - Clicked 'Review'")
                
                # B. Wait for "Approve" (FAB) button
                # Target: <button id="buttonApprove" ...>
                print("   - Waiting for 'Approve' button...")
                # Extra buffer wait for animation/loading
                time.sleep(1) 
                approve_btn = wait_instance.until(
                    EC.element_to_be_clickable((By.ID, "buttonApprove"))
                )
                # Ensure it is really clickable
                time.sleep(0.5) 
                approve_btn.click()
                print("   - Clicked 'Approve'")
                
                # C. Wait for SweetAlert Modal "Ya" button
                # Target: <button ... class="swal2-confirm ...">Ya</button>
                print("   - Waiting for confirmation modal...")
                confirm_btn = wait_instance.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm"))
                )
                time.sleep(0.5) # Stability pause
                confirm_btn.click()
                print("   - Clicked 'Ya' (Confirmed)")
                
                # Wait a moment for the action to register before moving on
                time.sleep(2)
                return True
                
            except Exception as e:
                print(f"   ! Error on this row: {e}")
                # Optional: print traceback if needed for debugging
                # import traceback
                # traceback.print_exc()
                return False

        # First Passthrough
        print("\n--- Starting First Pass ---")
        for i, row in enumerate(rows):
            success = process_row(i, row, driver, wait)
            if not success:
                failed_rows.append((i, row))

        # Retry Logic
        if failed_rows:
            print("\n" + "="*50)
            print(f"Finished first pass. {len(failed_rows)} items failed.")
            print("Retrying failed items now...")
            print("="*50)
            
            still_failed = []
            for i, row in failed_rows:
                print(f"\nRetrying Row {i+1}...")
                success = process_row(i, row, driver, wait)
                if not success:
                    still_failed.append((i, row))
            
            if still_failed:
                print("\n" + "="*50)
                print(f"Retry pass finished. {len(still_failed)} items STILL failed.")
                print("Please check these manually:")
                for i, row in still_failed:
                    print(f" - Row {i+1}: {row.get('Assignment Link', 'No Link')}")
            else:
                print("\n" + "="*50)
                print("All failed items were successfully processed on retry!")
        else:
            print("\n" + "="*50)
            print("All items processed successfully on first pass!")

        print("="*50)
        print("Automation finished.")
        
    except KeyboardInterrupt:
        print("\nScript stopped by user.")
    finally:
        # Ask to close
        input("Press ENTER to close the browser...")
        driver.quit()

if __name__ == "__main__":
    main()
