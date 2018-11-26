import sys
import cv2
from ReinventingTheWheel.tone_curve import ToneCurve

def preview(image):
    cv2.imshow("preview",image) #画像出力 imshow(window_name, image)
    cv2.waitKey()             #キー入力待ち waitKey(delay=0)
    cv2.destroyAllWindows()   #ウィンドウを消す destroyAllWindows()

'''
BGR の順。
image[:, :, (0,2)] = 0
の場合、(0,2) すなわち、全ての Blue と Red が選択されて、0が代入される。
結果として、緑以外の色がなくなる（緑だけの画像になる）
'''

if __name__ == "__main__":
    args = sys.argv
    
    # 画像読み込み
    image = cv2.imread(args[1]) / 255

    # 画像を編集
    tc = ToneCurve()
    image_edit = tc.tone_curve(image, 2)
    print(image)
    print(image_edit)


    # 画像表示
    preview(image_edit)
    
    #画像保存 imwrite(filename, image)
    cv2.imwrite("result/result.jpg",image_edit)





