
import telepot
from io import BytesIO
from PIL import Image
from PIL import ImageGrab
import numpy as np
import cv2
from pynput.keyboard import Key, Controller
import time
# import values for paths and token from values.py in the same folder
import amazon
#initialize and wait
keyboard = Controller()
time.sleep(5)
# computer vision for template matching
# libraries to take screenshots
# import telepot to send a message when shiny found
bot = telepot.Bot(amazon.TOKEN)


def computer_vision():
    # import the image of the shiny pokemon
    shiny_png = np.array(cv2.imread(amazon.SHINY_PATH, cv2.IMREAD_UNCHANGED))
    
    # take a screenshot of the main screen
    screen = ImageGrab.grab()
    screenshot = np.array(screen)
    # save the screenshot for future visual checks
    save_screenshot = np.array(screen)
    # convert images in order to check if shiny is presentp
    shiny_png = cv2.cvtColor(shiny_png, cv2.COLOR_RGB2BGR)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    # looking for the shiny
    result = cv2.matchTemplate(screenshot, shiny_png, cv2.TM_CCOEFF_NORMED)

    # max_val = max percentage of similarity
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print('matching ' + str(round(max_val*100, 2)) + '%')
    # format the screenshot in order to save it anyway
    new_p = Image.fromarray(save_screenshot)
    if new_p.mode != 'RGB':
        new_p = new_p.convert('RGB')
    # create the name of the screenshot
    photoname = str(round(max_val*100, 2)) + "mudkip" + \
        str(round(time.time()/1000, 2))[:-2]+".jpeg"
    # save the screenshot to the path
    path = amazon.SCREEN_PATH + photoname
    new_p.save(path)
    # check if the shiny is found
    threshold = 0.94
    if(max_val > threshold):
        return True
    else:
        # if found shiny send photo with the pyhton bot
        bot.sendPhoto(amazon.CHAT_ID, open(path, 'rb'))
        return False


def redo():   # reset, start game, select the rightest pokeball (for mudkip) and start the battl
        
    keyboard.press(Key.ctrl)
    keyboard.press('r')
        # a bit of delay between pressing and releasing to simulate better
    time.sleep(0.1)
    keyboard.release(Key.ctrl)
    keyboard.release('r')
        # wait a bit until the next key
        


def main():
    # open the text file to save the number of resets
    # while no shiny found
    while(computer_vision()):
        # delay the next cycle
        time.sleep(15)
        redo()
        time.sleep(15)
        # update the resets count
    # when shiny found the program exists

if __name__ == '__main__':
    main()
