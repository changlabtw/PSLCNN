from selenium import webdriver
import time
import sys
#GO:0008150, GO:0055085, GO:0006811, GO:0006520
print ('list:', str(sys.argv[1]))
print("$('textarea.default').val(" + str(sys.argv[1]) + ")")
driver = webdriver.Chrome('/Users/eric/chromedriver')

driver.get("https://www.ebi.ac.uk/QuickGO/slimming")

change_block = driver.find_element_by_link_text("Input your own")
change_block.click()
input = driver.find_element_by_tag_name('textarea')

print(input)
driver.execute_script("$('textarea.default').click()")

driver.execute_script("$('textarea.default').val('" + str(sys.argv[1]) + "')")
count = 0
for i in driver.find_elements_by_tag_name("textarea"):
    if count == 0:
        i.send_keys(u'\ue00d')
        count = count +1

driver.execute_script("$('button.button').removeAttr('disabled');")
count = 0
for i in driver.find_elements_by_xpath("//*[contains(text(), 'Add terms to selection')]"):
    count = count + 1
    print(i)
    if count == 2:
        i.click()

# driver.find_element_by_link_text("Add terms to selection").click()
time.sleep(5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(1)

driver.find_element_by_class_name('chart-btn').click()
time.sleep(3)
base_str = driver.find_element_by_id('ancestorChart').get_attribute("ng-src")
print(base_str)

html = driver.page_source       # get html
driver.get_screenshot_as_file("./sreenshot1.png")
driver.close()
return base_str
