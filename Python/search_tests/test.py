import numpy as np

"""
test_arr = [
    [1,4,3],
    [465,2,4]
]

print(test_arr)
print(2 * test_arr)

test_arr = np.array(test_arr)
print()

print(test_arr)
print(2 * test_arr)
"""

import cv2

def preview(image):
    cv2.imshow("preview",image) #画像出力 imshow(window_name, image)
    cv2.waitKey()             #キー入力待ち waitKey(delay=0)
    cv2.destroyAllWindows()   #ウィンドウを消す destroyAllWindows()


# 画像読み込み
image = cv2.imread('original.jpg') #/ 255
# 画像表示
preview(image)

