import cv2
import numpy as np

piano_tile = cv2.imread("piano_tile.PNG", cv2.IMREAD_UNCHANGED)
test_ss = cv2.imread("test_ss.PNG", cv2.IMREAD_UNCHANGED)
cv2.imshow('Piano Tiles', test_ss)
cv2.waitKey()
cv2.destroyAllWindows()
find_click_spots = cv2.matchTemplate(test_ss, piano_tile, cv2.TM_CCORR_NORMED)
cv2.imshow('Piano Tiles', find_click_spots)
cv2.waitKey()
cv2.destroyAllWindows()
worst_value, best_value, worst_location, best_location = cv2.minMaxLoc(find_click_spots)
print(best_value, "  best loc: " , best_location)
w = piano_tile.shape[1]
h = piano_tile.shape[0]
threshold = 0.971
tile_y, tile_x = np.where(find_click_spots >= threshold)
print(len(tile_x))
duplicates = []
for (x,y) in zip(tile_x, tile_y):
    print(x,y)
    duplicates.append([int(x),int(y), int(w), int(h)])
    duplicates.append([int(x),int(y), int(w), int(h)])
final_target_positions, useless = cv2.groupRectangles(duplicates, 1, 0.1)
print(len(final_target_positions))
for (x, y, w, h) in final_target_positions:
    cv2.rectangle(test_ss, (x,y), (x + w, y + h), (0,0,255), 5)
cv2.imshow('Piano Tiles', test_ss)
cv2.waitKey()
cv2.destroyAllWindows()

