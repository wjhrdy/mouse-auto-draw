import pyautogui
from time import sleep
from pynput import keyboard


brush = 10
canvas = (484, 213), (956, 650)
MODE = 1

if MODE == 1:
    def draw(img):
        click(565, 709)
        
        for current_color in colors:
            if current_color == (255, 255, 255) or current_color in bg_colors:
                continue
            change_color(current_color)
            for y, ly in enumerate(img):
                last_color = None
                for x, pixel_color in enumerate(ly):
                    pos = (x*brush+brush/2+canvas[0][0],
                           y*brush+brush/2+canvas[0][1])

                    if pixel_color == current_color:
                        if last_color != pixel_color:
                            pyautogui.moveTo(pos[0], pos[1])
                            pyautogui.mouseDown()
                        elif last_color == pixel_color:
                            pyautogui.moveTo(pos[0], pos[1])
                    elif last_color == current_color:
                        pyautogui.mouseUp()
                        # sleep(.0001)
                    last_color = pixel_color
                pyautogui.mouseUp()

elif MODE == 0:
    def draw(img):
        for y, ly in enumerate(img):
            for x, pixel_color in enumerate(ly):
                if pixel_color == (0, 0, 0):
                    continue
                change_color(pixel_color)
                click(x * brush + brush / 2 + canvas[0][0],
                      y * brush + brush / 2 + canvas[0][1])



def change_color(color):
    i = colors.index(color)
    x = 942 - i*40
    y = 174
    click(x, y)

def change_brushsize(size):
    pass

def click(x, y, t=.001):
    pyautogui.click(x, y)
    sleep(t)


colors = ((255, 255, 255),
          (255, 0, 25), 
          (247, 236, 70),
          (0, 225, 132), 
          (21, 54, 177), 
          (102, 74, 41),
          (208, 0, 250), 
          (0, 0, 0))

bg_colors = ((39,79,156),
    (95,98,103),
    (8,8,8),
    (117,14,30),
    (98,92,74))
