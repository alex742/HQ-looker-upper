You will need to type the following into the command prompt:

pip install puautogui
pip install selenium

You need to install the PhantomJS browser and add it to your system path variable. You will need to restart the command
prompt once you have done this.

When you run the program it will open up and load all of the browser stuff first, then hit enter to run.
Steps of program:

1 - Takes screenshot of your screen. I have it set up so that it works with a streaming app (ScreenMeet) if you stream
to a window in the right half of your screen.

2 - Saves the screenshot

3 - Crops and saves 3 screenshots, 1 for the question, and 3 for the answers (you might need to mess around with the values
on lines 22 - 26).

4 - Use OCR to convert screenshots to text. ############## DOES NOT WORK YET

5 - Search for the question using selenium

6 - count the answers (literally counting number of times each answer appears in all text) ########## DOES NOT WORK YET

7 - calculate probabilities (count/total * 100)

8 - Output

9 - Hit enter to run it again, type q then hit enter to quit (or CTRL + C).