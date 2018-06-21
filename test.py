import selenium.webdriver as webdriver

def getResults(searchTerm, numResults = 3):
	url = "https://www.startpage.com/"
	browser = webdriver.PhantomJS()
	browser.get(url)
	searchBox = browser.find_element_by_id("query")
	searchBox.send_keys(searchTerm)
	searchBox.submit()
	try:
		links = browser.find_elements_by_xpath("//ol[@class='web_regular_results']//h3//a")
	except:
		links = browser.find_elements_by_xpath("//h3///a")
	results = []
	for link in links[:numResults]:
		href = link.get_attribute("href")
		print(href)
		results.append(href)
	browser.close()
	return results

response = getResults("dog", 5)