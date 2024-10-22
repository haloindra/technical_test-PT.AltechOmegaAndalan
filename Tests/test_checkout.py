from Data import user_data
import pytest
import time
import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

@pytest.mark.checkout
class TestCheckout:

    
    def test_checkout(self):

        ######################################################################################################################
        # Login Section
        ######################################################################################################################
        # Initialize ChromeOptions and set desired options
        chrome_options = Options()
        chrome_options.add_argument('--headless') 
        chrome_options.add_argument('--no-sandbox')  # Required for some Linux environments
        chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited /dev/shm space issues

        # Use WebDriver Manager to manage the ChromeDriver version
        driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="130.0.6723.58").install()), options=chrome_options)


        driver.maximize_window()
        driver.get(user_data.URL)
        driver.implicitly_wait(user_data.implicit_wait_time)
        # Type username into Username field
        username_locator = driver.find_element(By.ID, "user-name")
        username_locator.send_keys(user_data.STANDARD_USER)
        # Type password into Password field
        password_locator = driver.find_element(By.NAME, "password")
        password_locator.send_keys(user_data.STANDARD_PASSWORD)
        # Submit
        submit_button_locator = driver.find_element(By.XPATH, "//input[@class='submit-button btn_action']")
        submit_button_locator.click()
        time.sleep(5)

        ######################################################################################################################
        # Cart Section
        ######################################################################################################################
        
        # Add Item To Cart   
        cart_one_locator = driver.find_element(By.XPATH, "//button[@id='add-to-cart-sauce-labs-backpack']")
        cart_one_locator.click()
        cart_two_locator = driver.find_element(By.XPATH, "//button[@id='add-to-cart-sauce-labs-bike-light']")
        cart_two_locator.click()
        cart_tree_locator = driver.find_element(By.XPATH, "//button[@id='add-to-cart-sauce-labs-bolt-t-shirt']")
        cart_tree_locator.click()
        
        # Click cart to go to shopping cart page
        cart_icon_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "shopping_cart_container")))
        cart_icon_locator.click()
        driver.implicitly_wait(user_data.implicit_wait_time)
        time.sleep(5)

        # Wait for the cart count element to be visible
        cart_count_locator  = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@class='shopping_cart_badge']"))
        )

        # Get the text of the cart count element
        cart_count_text = cart_count_locator.text

        # Convert the cart count text to an integer
        cart_count = int(cart_count_text)

        # Verify if the cart count is equal to expected_items_count
        expected_items_count = 3
        if cart_count == expected_items_count:
            print(f"There are {expected_items_count} items in the cart.")
            # Assert that the cart count is 3
            assert cart_count == expected_items_count, "There are not 3 items in the cart."     
        else:
            print(f"There are not {expected_items_count} items in the cart.")


        # Validation: Check product names and prices in the cart
        product_name_locators = driver.find_elements(By.XPATH, "//div[@class= 'inventory_item_name']")

        # Find all product price elements in the cart
        product_price_locators = driver.find_elements(By.XPATH, "//div[@class= 'inventory_item_price']")

        # Define expected product names and prices (for demonstration purposes)
        expected_product_names = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
        expected_product_prices = ["$29.99", "$9.99", "$15.99"]


        for index, (product_name_element, product_price_element, expected_name, expected_price) in enumerate (zip(product_name_locators, product_price_locators, expected_product_names, expected_product_prices)):
            product_name = product_name_element.text
            product_price = product_price_element.text

            # Perform validation for each product name and price
            assert product_name == expected_name, f"Expected product name: {expected_name}, Actual product name: {product_name}"
            # print(f"Expected product name: {expected_name}")
            assert product_price == expected_price, f"Expected product price: {expected_price}, Actual product price: {product_price}"
            # print(f"Expected product price: {expected_price}")

            print(f"Product Name {index +1}: {product_name}, Product Price: {product_price}")

        time.sleep(5)

        ######################################################################################################################
        # Checkout Section
        ######################################################################################################################
        # Click button checkout
        button_checkout = driver.find_element(By.XPATH, "//button[@id='checkout']")
        button_checkout.click()

        # Input User Information - if firstname not input - Negative Case 
        first_name_locator = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "first-name")))
        first_name_locator.send_keys(user_data.EMPTY_STRING)

        last_name_locator = driver.find_element(By.ID, "last-name")
        last_name_locator.send_keys(user_data.LASTNAME)

        zipcode_locator = driver.find_element(By.ID, "postal-code")
        zipcode_locator.send_keys(user_data.ZIP)

        button_continue_locator = driver.find_element(By.NAME, "continue")
        button_continue_locator.click()

        # Validation eror message
        error_message = driver.find_element(By.XPATH, "//div[@class= 'error-message-container error']").text
        assert "Error: First Name is required" in error_message, f"Error message is not expected. It should show : {error_message}"
        time.sleep(5)   
        
        # Input User Information - Positive Case
        first_name_locator.send_keys(user_data.FIRSTNAME)
        last_name_locator.send_keys(user_data.LASTNAME)
        zipcode_locator.send_keys(user_data.ZIP)
        button_continue_locator.click()
        time.sleep(5)
        
        # Validation Subtitle Checkout: Overview 
        checkout_page_title_locator = driver.find_element(By.XPATH, "//span[contains(text(),'Checkout: Overview')]")
        assert checkout_page_title_locator.text == "Checkout: Overview", "Cheackout Title page is not expected."
        
        
        # Subtotal Calculation
        # Get all price from class inventory_item_price
        subtotal_locators = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_price"))
        )

        # Initialize subtotal
        subtotal = 0.0

        # Iterate through each subtotal locator
        for price_locator in subtotal_locators:
            # Get the text of the price
            price_text = price_locator.text
            
            # Remove any currency symbols from the price text
            price_text = price_text.replace('$',"")  # In This case of saucedemo.com currency symbol is $
            
            # Convert the price text to a float and add it to the subtotal
            subtotal += float(price_text)

        # Print the subtotal
        print(f"Subtotal is :", subtotal)

        expected_total = 55.97  
        assert subtotal == expected_total, print(f"Subtotal is not expected. Actual Subtotal is : {subtotal}, Expected is: {expected_total}")

        print(f"Expected Subtotal is :", subtotal)
        time.sleep(10)

        # Submit Checkout
        button_finish_locator = driver.find_element(By.ID, "finish")
        button_finish_locator.click()
        
        # Validation Success Checkout 
        checkout_complete_title_locator = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Checkout: Complete!')]"))
            )
        assert checkout_complete_title_locator.text == "Checkout: Complete!", "Title is not expected."
        assert driver.find_element(By.XPATH, "//h2[contains(text(),'Thank you for your order!')]").text == "Thank you for your order!", "Teks deskripsi tidak sesuai."
        

        # Validation Cart item after Checkout

        # Initialize cart_items_count
        cart_items_count = 0

        try:
            # Find all cart items
            cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")

            # Get the number of cart items
            cart_items_count = len(cart_items)

            expected_items_after_checkout = 0
            if cart_items_count == expected_items_after_checkout:
                # Print the number of cart items
                print(f"Validation Pass : There are {cart_items_count} items found in Cart after Checkout Finish")
                assert cart_items_count == expected_items_after_checkout, "There are items in the cart."
            else:
                print(f"Validation Fail : Number of cart items: {cart_items_count}")
                
        except NoSuchElementException:
            print(f"Validation Exeption is Pass : There are {cart_items_count} items found")

        # Close the browser
        driver.quit()



