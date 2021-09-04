from selenium import webdriver

driver = webdriver.Chrome(executable_path="C:\Automation\chromedriver.exe")

driver.get("https://git-scm.com")
print(driver.title)
print(driver.current_url)
driver.close()