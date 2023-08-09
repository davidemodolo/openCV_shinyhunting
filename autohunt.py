# ------------------------------------
# TODO:
# - shiny file RGB and not BRG
# - normalize dimension
# - check only on the emulator window
# ------------------------------------

# libraries to simulate pressing keys
import telepot
from PIL import Image
from PIL import ImageGrab
import numpy as np
import cv2
from pynput.keyboard import Controller
import time
# import values for paths and token from values.py in the same folder
import values
#initialize
bot = telepot.Bot(values.TOKEN) # to receive the photo on telegram when a shiny is found
keyboard = Controller()

commands = {
    'leafgreen':{
        'squirtle': "rnxxxxnxxxxxxxxxxnznxnxexxxn",
        'charmander': "rnxxxxnxxxxxxxxxzznznxnxexxxn"
    },
    'sapphire':{
        'mudkip': "rnxxxxxdxxnxn"
    }
}

LONGER_DELAY = 'n'
EMU_SPEED = 10
GAME = 'sapphire'
POKEMON = 'mudkip'
SAVESTATE = '1'
PAUSE = 'p'
PROBABILITY = 8196
THRESHOLD = 0.99

shiny_png = np.array(cv2.imread(values.SHINY_PATH, cv2.IMREAD_UNCHANGED))
shiny_png = cv2.cvtColor(shiny_png, cv2.COLOR_BGRA2BGR)

POOCHYENA = True
if POOCHYENA:
    poochyena = np.array(cv2.imread("poochyena_sapphire.png", cv2.IMREAD_UNCHANGED))
    poochyena = cv2.cvtColor(poochyena, cv2.COLOR_BGRA2BGR)

def computer_vision(reset_count):
    screen = ImageGrab.grab()
    screenshot = np.array(screen)
    screenshot_to_send = Image.fromarray(screenshot)

    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    result = cv2.matchTemplate(screenshot, shiny_png, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    print(f'\nmatching {POKEMON} ' + str(round(max_val*100, 2)) + '%')

    max_val_p = 1
    if POOCHYENA:
        result_poochyena = cv2.matchTemplate(screenshot, poochyena, cv2.TM_CCOEFF_NORMED)
        min_val_p, max_val_p, min_loc_p, max_loc_p = cv2.minMaxLoc(result_poochyena)
        print('matching poochyena ' + str(round(max_val_p*100, 2)) + '%')

    photoname = POKEMON + f"{reset_count}" +".png"
    path = values.SCREEN_PATH + photoname

    if(max_val > THRESHOLD and max_val_p > THRESHOLD):
        return True
    else:
        screenshot_to_send.save(path)
        bot.sendPhoto(values.CHAT_ID, open(path, 'rb'))
        return False


def redo():
    for cr in commands[GAME][POKEMON]:
        key = str(cr)
        if not (key == LONGER_DELAY):
            time.sleep(1/EMU_SPEED)
        else:
            time.sleep(5/EMU_SPEED)
        keyboard.press(key)
        time.sleep(0.1)
        keyboard.release(key)

def main():
    time.sleep(5)
    path = values.RESETS_PATH
    file_resets = open(path, "r")
    resets_count = int(file_resets.read())
    file_resets.close()
    while(computer_vision(resets_count)):
        time.sleep(2)
        redo()
        resets_count = resets_count + 1
        file_resets = open(path, "w")
        file_resets.write(str(resets_count))
        print(str(resets_count) + " resets: " +
              str(round((resets_count*100/PROBABILITY), 3))+"% to find a shiny")

    keyboard.press(PAUSE)
    time.sleep(0.1)
    keyboard.release(PAUSE)
    keyboard.press(SAVESTATE)
    time.sleep(0.1)
    keyboard.release(SAVESTATE)
    print('SHINY after ' + str(resets_count) + ' soft resets')


if __name__ == '__main__':
    main()
