# 📦 Required Libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import json
import time
from datetime import datetime

# ✅ Chrome Setup
options = Options()
options.add_argument("--headless")  # Run headless (background)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")

# ✅ Initialize Chrome Driver
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# ✅ Data List
all_data = []

# ✅ Scrape Pages
for page in range(1, 3):  # Change 3 to 676 to scrape all pages
    print(f"📄 Scraping page {page}...")
    url = f"https://www.flipkart.com/clothing-and-accessories/topwear/tshirt/men-tshirt/pr?sid=clo,ash,ank,edy&page={page}"
    driver.get(url)
    time.sleep(3)  # Allow page to load

    # ❌ Close login popup if it appears
    try:
        close_btn = driver.find_element(By.XPATH, '//button[text()="✕"]')
        close_btn.click()
        time.sleep(2)
    except:
        pass

    # ✅ Wait until product cards load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_1xHGtK"))
        )
        products = driver.find_elements(By.CLASS_NAME, "_1xHGtK")
    except:
        print(f"⚠️ No products found on page {page}")
        continue

    for product in products:
        try:
            title = product.find_element(By.CLASS_NAME, "IRpwTa").text
        except NoSuchElementException:
            title = None

        try:
            discounted_price = product.find_element(By.CLASS_NAME, "_30jeq3").text
        except NoSuchElementException:
            discounted_price = None

        try:
            original_price = product.find_element(By.CLASS_NAME, "_3I9_wc").text
        except NoSuchElementException:
            original_price = None

        try:
            discount_percent = product.find_element(By.CLASS_NAME, "_3Ay6Sb").text
        except NoSuchElementException:
            discount_percent = None

        try:
            deal_tag = product.find_element(By.CLASS_NAME, "_2Tpdn3").text
        except NoSuchElementException:
            deal_tag = None

        try:
            size_text = product.find_element(By.CLASS_NAME, "_3eWWd6").text
            sizes = size_text.replace("Size", "").replace(" ", "").split(",")
        except NoSuchElementException:
            sizes = []

        all_data.append({
            "product_title": title,
            "discounted_price": discounted_price,
            "original_price": original_price,
            "discount_percentage": discount_percent,
            "deal_tag": deal_tag,
            "available_sizes": sizes
        })

# ✅ Close browser
driver.quit()

# ✅ Data check
if not all_data:
    print("⚠️ No data scraped! Please check class names or network.")
else:
    print(f"✅ Total products scraped: {len(all_data)}")
    print("🔍 Preview:", json.dumps(all_data[:1], indent=2, ensure_ascii=False))

# ✅ Save the Data
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
json_file = f"flipkart_data_{timestamp}.json"
csv_file = f"flipkart_data_{timestamp}.csv"
excel_file = f"flipkart_data_{timestamp}.xlsx"

# Save as JSON
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=4, ensure_ascii=False)

# Save as CSV/Excel
df = pd.DataFrame(all_data)
df.to_csv(csv_file, index=False, encoding='utf-8-sig')
df.to_excel(excel_file, index=False)

# ✅ Confirmation
print(f"📁 JSON saved as:  {json_file}")
print(f"📁 CSV saved as:   {csv_file}")
print(f"📁 Excel saved as: {excel_file}")

# Loop ke leye kia karna hogaaaaaaaa.......


