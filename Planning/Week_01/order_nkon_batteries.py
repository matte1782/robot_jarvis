"""
NKON Battery Order Automation Script
Automates ordering 2× Molicel INR18650-P30B batteries from NKON.nl
Stops at payment page for manual credit card entry
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

# User information
USER_INFO = {
    'name': 'Matteo Panzeri',
    'address': 'Via canonica 3',
    'city': 'Monza',
    'postal_code': '20900',
    'country': 'Italy',
    'phone': '3356274958',
    'email': 'matteo1782@gmail.com'
}

def wait_for_element(driver, by, value, timeout=10):
    """Wait for element to be present and visible"""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def wait_for_clickable(driver, by, value, timeout=10):
    """Wait for element to be clickable"""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )

def order_batteries():
    """Main automation function"""

    print("🚀 Starting NKON battery order automation...")
    print(f"📋 Order details:")
    print(f"   - Product: Molicel INR18650-P30B")
    print(f"   - Quantity: 2")
    print(f"   - Solder tags: GEEN (none)")
    print(f"   - Total: €7.98")
    print()

    # Initialize Chrome driver
    print("🌐 Opening browser...")
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)

    try:
        # Step 1: Go to NKON.nl
        print("📍 Navigating to NKON.nl...")
        driver.get("https://www.nkon.nl/")
        time.sleep(2)

        # Accept cookies if popup appears
        try:
            cookie_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Accepteren')]")
            cookie_button.click()
            print("✅ Accepted cookies")
            time.sleep(1)
        except:
            print("ℹ️  No cookie popup found")

        # Step 2: Search for battery
        print("🔍 Searching for Molicel INR18650-P30B...")
        search_box = wait_for_element(driver, By.NAME, "search")
        search_box.clear()
        search_box.send_keys("Molicel INR18650-P30B")
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        # Step 3: Click on product
        print("📦 Opening product page...")
        product_link = wait_for_clickable(driver, By.XPATH, "//a[contains(@href, 'molicel') or contains(text(), 'Molicel')]")
        product_link.click()
        time.sleep(2)

        # Step 4: Select "GEEN" for solder tags (if option exists)
        print("⚙️  Selecting solder tag option: GEEN (none)...")
        try:
            # Look for radio button or dropdown for solder tags
            geen_option = driver.find_element(By.XPATH, "//label[contains(text(), 'Geen')]//input | //option[contains(text(), 'Geen')]")
            geen_option.click()
            print("✅ Selected: GEEN (no solder tags)")
            time.sleep(1)
        except:
            print("ℹ️  Solder tag option not found or already set to GEEN")

        # Step 5: Set quantity to 2
        print("🔢 Setting quantity to 2...")
        try:
            quantity_input = driver.find_element(By.NAME, "quantity")
            quantity_input.clear()
            quantity_input.send_keys("2")
            print("✅ Quantity set to 2")
            time.sleep(1)
        except:
            print("⚠️  Could not find quantity field, might be default")

        # Step 6: Add to cart
        print("🛒 Adding to cart...")
        add_to_cart_button = wait_for_clickable(driver, By.XPATH, "//button[contains(text(), 'In winkelwagen') or contains(text(), 'Add to cart')]")
        add_to_cart_button.click()
        time.sleep(3)

        print("✅ Added to cart!")

        # Step 7: Go to cart
        print("🛒 Going to cart...")
        cart_button = wait_for_clickable(driver, By.XPATH, "//a[contains(@href, 'cart') or contains(@href, 'winkelwagen')]")
        cart_button.click()
        time.sleep(2)

        # Step 8: Proceed to checkout
        print("💳 Proceeding to checkout...")
        checkout_button = wait_for_clickable(driver, By.XPATH, "//a[contains(text(), 'Afrekenen') or contains(text(), 'Checkout')]")
        checkout_button.click()
        time.sleep(3)

        # Step 9: Fill in shipping information
        print("📝 Filling in shipping information...")

        # Name
        try:
            name_parts = USER_INFO['name'].split()
            firstname = name_parts[0]
            lastname = ' '.join(name_parts[1:])

            firstname_field = driver.find_element(By.NAME, "firstname")
            firstname_field.clear()
            firstname_field.send_keys(firstname)

            lastname_field = driver.find_element(By.NAME, "lastname")
            lastname_field.clear()
            lastname_field.send_keys(lastname)

            print(f"   ✅ Name: {USER_INFO['name']}")
        except Exception as e:
            print(f"   ⚠️  Name fields: {e}")

        # Email
        try:
            email_field = driver.find_element(By.NAME, "email")
            email_field.clear()
            email_field.send_keys(USER_INFO['email'])
            print(f"   ✅ Email: {USER_INFO['email']}")
        except Exception as e:
            print(f"   ⚠️  Email field: {e}")

        # Phone
        try:
            phone_field = driver.find_element(By.NAME, "telephone")
            phone_field.clear()
            phone_field.send_keys(USER_INFO['phone'])
            print(f"   ✅ Phone: {USER_INFO['phone']}")
        except Exception as e:
            print(f"   ⚠️  Phone field: {e}")

        # Address
        try:
            address_field = driver.find_element(By.NAME, "street")
            address_field.clear()
            address_field.send_keys(USER_INFO['address'])
            print(f"   ✅ Address: {USER_INFO['address']}")
        except Exception as e:
            print(f"   ⚠️  Address field: {e}")

        # Postal Code
        try:
            postcode_field = driver.find_element(By.NAME, "postcode")
            postcode_field.clear()
            postcode_field.send_keys(USER_INFO['postal_code'])
            print(f"   ✅ Postal Code: {USER_INFO['postal_code']}")
        except Exception as e:
            print(f"   ⚠️  Postal code field: {e}")

        # City
        try:
            city_field = driver.find_element(By.NAME, "city")
            city_field.clear()
            city_field.send_keys(USER_INFO['city'])
            print(f"   ✅ City: {USER_INFO['city']}")
        except Exception as e:
            print(f"   ⚠️  City field: {e}")

        # Country
        try:
            country_select = Select(driver.find_element(By.NAME, "country_id"))
            country_select.select_by_visible_text("Italy")
            print(f"   ✅ Country: {USER_INFO['country']}")
        except Exception as e:
            print(f"   ⚠️  Country field: {e}")

        time.sleep(2)

        # Step 10: Continue to payment
        print("💳 Proceeding to payment page...")
        try:
            continue_button = wait_for_clickable(driver, By.XPATH, "//button[contains(text(), 'Continue') or contains(text(), 'Doorgaan')]")
            continue_button.click()
            time.sleep(3)
        except:
            print("ℹ️  Continue button not needed")

        print()
        print("=" * 60)
        print("✅ AUTOMATION COMPLETE!")
        print("=" * 60)
        print()
        print("📋 Order Summary:")
        print(f"   - Product: Molicel INR18650-P30B")
        print(f"   - Quantity: 2×")
        print(f"   - Solder tags: GEEN (none)")
        print(f"   - Total: €7.98")
        print()
        print(f"📧 Shipping to:")
        print(f"   {USER_INFO['name']}")
        print(f"   {USER_INFO['address']}")
        print(f"   {USER_INFO['postal_code']} {USER_INFO['city']}")
        print(f"   {USER_INFO['country']}")
        print(f"   Phone: {USER_INFO['phone']}")
        print(f"   Email: {USER_INFO['email']}")
        print()
        print("💳 NEXT STEPS:")
        print("   1. Review all information on screen")
        print("   2. Select payment method")
        print("   3. Enter credit card details manually")
        print("   4. Complete payment")
        print("   5. Save order confirmation email")
        print()
        print("⚠️  Browser will stay open - DO NOT CLOSE until payment complete!")
        print()

        # Keep browser open
        input("Press ENTER when payment is complete to close browser...")

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        print("⚠️  You may need to complete the process manually")
        input("Press ENTER to close browser...")

    finally:
        driver.quit()
        print("✅ Browser closed")

if __name__ == "__main__":
    print()
    print("=" * 60)
    print("  NKON BATTERY ORDER AUTOMATION")
    print("=" * 60)
    print()
    print("⚠️  IMPORTANT:")
    print("   - This script automates form filling ONLY")
    print("   - You MUST complete payment manually")
    print("   - Review all information before payment")
    print()

    response = input("Ready to start? (yes/no): ")
    if response.lower() in ['yes', 'y', 'si', 'sì']:
        print()
        order_batteries()
    else:
        print("❌ Cancelled by user")
