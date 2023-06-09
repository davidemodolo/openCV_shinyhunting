# ------------------------------------
# TODO:
# - shiny file RGB and not BRG
# - normalize dimension
# - check only on the emulator window
# ------------------------------------

# libraries to simulate pressing keys
import telepot
from io import BytesIO
from PIL import Image
from PIL import ImageGrab
import numpy as np
import cv2
from pynput.keyboard import Key, Controller
import time
# import values for paths and token from values.py in the same folder
import values
#initialize and wait
keyboard = Controller()
time.sleep(5)
# computer vision for template matching
# libraries to take screenshots
# import telepot to send a message when shiny found
bot = telepot.Bot(values.TOKEN)


def computer_vision():
    # import the image of the shiny pokemon
    shiny_png = np.array(cv2.imread(values.SHINY_PATH, cv2.IMREAD_UNCHANGED))
    
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
    path = values.SCREEN_PATH + photoname
    new_p.save(path)
    # check if the shiny is found
    threshold = 0.99
    if(max_val > threshold):
        return True
    else:
        # if found shiny send photo with the pyhton bot
        bot.sendPhoto(values.CHAT_ID, open(path, 'rb'))
        return False


def redo():
    EMU_SPEED = 10  # emerald emulator speed
    # reset, start game, select the rightest pokeball (for mudkip) and start the battle
    commands = "rnxxxxnxxxxxxxxxxnznxnxexxxn"
    for cr in commands:
        key = str(cr)
        if not (key == 'n'):
            time.sleep(1/EMU_SPEED)
        else:
            time.sleep(5/EMU_SPEED)
        # simulate each key pressed
        
        
        keyboard.press(key)
        # a bit of delay between pressing and releasing to simulate better
        time.sleep(0.1)
        keyboard.release(key)
        # wait a bit until the next key
        


def main():
    # open the text file to save the number of resets
    path = values.RESETS_PATH
    file_resets = open(path, "r")
    resets_count = int(file_resets.read())
    file_resets.close()
    # while no shiny found
    while(computer_vision()):
        # delay the next cycle
        time.sleep(2)
        redo()
        # update the resets count
        resets_count = resets_count + 1
        file_resets = open(path, "w")
        file_resets.write(str(resets_count))
        # log on the console with the probability based on the 1/8192 shiny prob.
        print(str(resets_count) + " resets: " +
              str(round((resets_count*100/8192), 3))+"% to find a shiny")
    # when shiny found the program exists
    key = 'p'
    keyboard.press(key)
    time.sleep(0.1)
    keyboard.release(key)
    print('SHINY after ' + str(resets_count) + ' soft resets')


if __name__ == '__main__':
    main()
