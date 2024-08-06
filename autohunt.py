# ------------------------------------
# TODO:
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
        'squirtle': "rnxxxxnxxxxxxxxxxnznxnxexxxn", # FOUND AFTER 2848
        'charmander': "rnxxxxxnxxxxzznzznxnexxxn", # FOUND AFTER 18096
        'dratini': "rnxxxxxxxzzzxxsssxxzzesxxxnsn", # FOUND AFTER 11368
        'ghastly': "rnxxxnxzzn"+"wwwsss"*10+"nn", #
        'snorlax': "rnxxxnxzznxxnnnnnnnxnn"
    },
    'firered':{
        # 'bulbasaur': "rnxxxnxxzznxxxxnzzzzzzexxxn", # 
        'bulbasaur': "rnxxxnxzxxxxxzznzzexxxn", # found after 1428
    },
    'sapphire':{
        'mudkip': "rnxxxxxdxxnxn" # 8445
    }
}

LONGER_DELAY = 'n'
EMU_SPEED = 29
GAME = 'leafgreen'
POKEMON = 'snorlax'
POOCHYENA = False
SAVESTATE = '1'
PAUSE = 'p'
PROBABILITY = 8192
THRESHOLD = 0.999

shiny_png = np.array(cv2.imread(values.SHINY_PATH, cv2.IMREAD_UNCHANGED))
shiny_png = cv2.cvtColor(shiny_png, cv2.COLOR_BGRA2BGR)


if POOCHYENA:
    poochyena = np.array(cv2.imread("poochyena_sapphire.png", cv2.IMREAD_UNCHANGED))
    poochyena = cv2.cvtColor(poochyena, cv2.COLOR_BGRA2BGR)

def computer_vision(reset_count):
    screen = ImageGrab.grab(all_screens=True)
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

    if(max_val > THRESHOLD and max_val_p > THRESHOLD): # it's classic
        return True
    else: # may be shiny
        # shiny_png_cubone = np.array(cv2.imread("cubone.png", cv2.IMREAD_UNCHANGED))
        # shiny_png_cubone = cv2.cvtColor(shiny_png_cubone, cv2.COLOR_BGRA2BGR)
        # result = cv2.matchTemplate(screenshot, shiny_png_cubone, cv2.TM_CCOEFF_NORMED)
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # print('\nmatching Cubone ' + str(round(max_val*100, 2)) + '%')
        # if(max_val > THRESHOLD):
        #     return True
        
        # shiny_png_player = np.array(cv2.imread("player.png", cv2.IMREAD_UNCHANGED))
        # shiny_png_player = cv2.cvtColor(shiny_png_player, cv2.COLOR_BGRA2BGR)
        # result = cv2.matchTemplate(screenshot, shiny_png_player, cv2.TM_CCOEFF_NORMED)
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # print('\nmatching Player ' + str(round(max_val*100, 2)) + '%')
        # if(max_val > THRESHOLD):
        #     return True
        
        # # same for haunter
        # shiny_png_haunter = np.array(cv2.imread("haunter.png", cv2.IMREAD_UNCHANGED))
        # shiny_png_haunter = cv2.cvtColor(shiny_png_haunter, cv2.COLOR_BGRA2BGR)
        # result = cv2.matchTemplate(screenshot, shiny_png_haunter, cv2.TM_CCOEFF_NORMED)
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # print('\nmatching Haunter ' + str(round(max_val*100, 2)) + '%')
        # if(max_val > THRESHOLD):
        #     return True
        screenshot_to_send.save(path)
        bot.sendPhoto(values.CHAT_ID, open(path, 'rb'))
        return False


def redo():
    for cr in commands[GAME][POKEMON]:
        key = str(cr)
        # print(key)
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
        time.sleep(1)
        redo()
        resets_count = resets_count + 1
        file_resets = open(path, "w")
        file_resets.write(str(resets_count))
        file_resets.close()
        print(str(resets_count) + " resets: " +
              str(round((resets_count*100/PROBABILITY), 3))+"% to find a shiny")
    resets_count = resets_count + 1
    file_resets = open(path, "w")
    file_resets.write(str(resets_count))
    file_resets.close()
    keyboard.press(PAUSE)
    time.sleep(0.1)
    keyboard.release(PAUSE)
    keyboard.press(SAVESTATE)
    time.sleep(0.1)
    keyboard.release(SAVESTATE)
    print('SHINY after ' + str(resets_count) + ' soft resets')


if __name__ == '__main__':
    main()
