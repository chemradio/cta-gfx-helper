from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') 
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.headless = True
driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=chrome_options)
# driver = webdriver.Remote("http://localhost:4444/", options=chrome_options)


driver.get('https://google.com')
driver.save_screenshot('temp.png')
print('good')


