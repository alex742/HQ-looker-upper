import pyautogui
from PIL import Image
import selenium.webdriver as webdriver

url = "https://www.startpage.com/"
browser = webdriver.PhantomJS()

#these 3 lines are to load everything before the first q to make it run faster
key = ""
while key != 'q':
	key = input('')

	#take screenshot
	pic = pyautogui.screenshot()

	#save screenshot
	pic.save('screenshot.png')

	#break into multiple images
	image = Image.open('screenshot.png')

	width = 500
	qHeight = 230
	aHeight = 90
	xOrigin = 1200
	yOrigin = 270

	box = (xOrigin, yOrigin, xOrigin + width, yOrigin + qHeight)
	crop = image.crop(box)
	crop.save('question.png')

	box = (xOrigin, yOrigin + qHeight, xOrigin + width, yOrigin + qHeight + aHeight)
	crop = image.crop(box)
	crop.save('answer1.png')

	box = (xOrigin, yOrigin + qHeight + aHeight, xOrigin + width, yOrigin + qHeight + aHeight + aHeight)
	crop = image.crop(box)
	crop.save('answer2.png')

	box = (xOrigin, yOrigin + qHeight + (aHeight * 2), xOrigin + width, yOrigin + qHeight + aHeight + aHeight + aHeight)
	crop = image.crop(box)
	crop.save('answer3.png')

	#convert to text
	qText = ""
	a1Text = ""
	a2Text = ""
	a3Text = ""

	#search question
	browser.get(url)
	searchBox = browser.find_element_by_id("query")
	searchBox.send_keys(qText)
	searchBox.submit()
	try:
		links = browser.find_elements_by_xpath("//ol[@class='web_regular_results']//h3//a")
	except:
		links = browser.find_elements_by_xpath("//h3///a")
	results = []
	for link in links:
		href = link.get_attribute("href")
		print(href)
		results.append(href)

	#count answers
	aTotal = 0
	bTotal = 0
	cTotal = 0
	total = 0

	for result in results:
		aTotal += result.count(a1Text)
		bTotal += result.count(a2Text)
		cTotal += result.count(a3Text)

	total = aTotal + bTotal + cTotal

	#calculate probabilities
	aProb = 0
	bProb = 0
	cProb = 0
	try:
		aProb = aTotal/total * 100
		bProb = bTotal/total * 100
		cProb = cTotal/total * 100
	except:
		print("")

	#output
	print("########################################")
	print("Total - " + str(total))
	print("A - " + str(aProb) + "% with " + str(aTotal))
	print("B - " + str(bProb) + "% with " + str(bTotal))
	print("C - " + str(cProb) + "% with " + str(cTotal))
	print("########################################")

browser.close()