#Screenshots
import pyautogui
from PIL import Image
import selenium.webdriver as webdriver

#Computer Vision
import io
import os
from google.cloud import vision
from google.cloud.vision import types
# Instantiates a client
client = vision.ImageAnnotatorClient()
# The name of the image files to annotate
question_image_file = os.path.join(
    os.path.dirname(__file__),
    'question.png')
answer1_image_file = os.path.join(
    os.path.dirname(__file__),
    'answer1.png')
answer2_image_file = os.path.join(
    os.path.dirname(__file__),
    'answer2.png')
answer3_image_file = os.path.join(
    os.path.dirname(__file__),
    'answer3.png')

url = "https://www.startpage.com/"
browser = webdriver.PhantomJS()

#these 3 lines are to load everything before the first q to make it run faster
key = ""
print('Ready')
while key != 'q':
	key = input('')

	#take screenshot
	pic = pyautogui.screenshot()

	#save screenshot
	pic.save('screenshot.png')

	#break into multiple images
	image = Image.open('screenshot.png')

	width = 350
	qHeight = 150
	aHeight = 70
	xOrigin = 1010
	yOrigin = 150

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

	# Loads the image into memory
	with io.open(question_image_file, 'rb') as question_image:
		question_content = question_image.read()
	with io.open(answer1_image_file, 'rb') as answer1_image:
		answer1_content = answer1_image.read()
	with io.open(answer2_image_file, 'rb') as answer2_image:
		answer2_content = answer2_image.read()
	with io.open(answer3_image_file, 'rb') as answer3_image:
		answer3_content = answer3_image.read()

	q_image = types.Image(content=question_content)
	a1_image = types.Image(content=answer1_content)
	a2_image = types.Image(content=answer2_content)
	a3_image = types.Image(content=answer3_content)

	# Performs label detection on the image file
	question_response = client.text_detection(image=q_image)
	question_texts = question_response.text_annotations
	answer1_response = client.text_detection(image=a1_image)
	answer1_texts = answer1_response.text_annotations
	answer2_response = client.text_detection(image=a2_image)
	answer2_texts = answer2_response.text_annotations
	answer3_response = client.text_detection(image=a3_image)
	answer3_texts = answer3_response.text_annotations

	print('\n"{}"'.format(question_texts[0].description))
	print('\n"{}"'.format(answer1_texts[0].description))
	print('\n"{}"'.format(answer2_texts[0].description))
	print('\n"{}"'.format(answer3_texts[0].description))


	#convert to text
	qText = question_texts[0].description
	a1Text = answer1_texts[0].description
	a2Text = answer2_texts[0].description
	a3Text = answer3_texts[0].description

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
