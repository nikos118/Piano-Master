import pyautogui as pg
import cv2
import numpy as np
import keyboard
import win32gui
import win32ui
import win32con


#Optimized for http://tanksw.com/piano-tiles/ on a 31.5 inch screen at 2560x1440 resolution

def window_cap():
    screen_width = 2560
    screen_height = 1440 
    fullscreen = None

    wDC = win32gui.GetWindowDC(fullscreen)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    DBM = win32ui.CreateBitmap()
    DBM.CreateCompatibleBitmap(dcObj, screen_width, screen_height )
    cDC.SelectObject(DBM)
    cDC.BitBlt((0,0),(screen_width, screen_height ) , dcObj, (0,0), win32con.SRCCOPY)
    signedIntsArray = DBM.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (screen_height,screen_width,4)

    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(fullscreen, wDC)
    win32gui.DeleteObject(DBM.GetHandle())

    img = img[...,:3]

    return img

piano_tile = cv2.imread("piano_tile.PNG", cv2.IMREAD_COLOR)
pg.PAUSE = 0.1
print("Press 'q' to exit at any time.")
while(True):

    if keyboard.is_pressed('q'):
        print("You pressed 'q', now exiting.")
        break

    screenshot = window_cap()

    find_click_spots = cv2.matchTemplate(screenshot, piano_tile, cv2.TM_CCORR_NORMED)

    worst_value, best_value, worst_location, best_location = cv2.minMaxLoc(find_click_spots)

    w = piano_tile.shape[1]
    h = piano_tile.shape[0]

    threshold = 0.65
    tile_y, tile_x = np.where(find_click_spots >= threshold)

    duplicates = []
    for (x,y) in zip(tile_x, tile_y):
        duplicates.append([int(x),int(y), int(w), int(h)])
        duplicates.append([int(x),int(y), int(w), int(h)])
    
    final_target_positions, useless = cv2.groupRectangles(duplicates, 1, 0.02)
 

    for (x, y, w, h) in final_target_positions:
        if keyboard.is_pressed('q'):
            print("You pressed 'q', now exiting.")
            break
        pg.click(x + w/2, y + h/2)
        








