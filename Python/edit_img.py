import sys
import cv2
import numpy as np

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

### トーンカーブ
def tone_curve(img, γ):
    return img**(1/γ)

### αブレンディング
def α_blending(imgs=[], αs=[]):
    # or sum(αs) != 1
    if len(imgs) < 2 or len(imgs) != len(αs):
        return []  # ほんとはエラー処理すべき

    # 0埋めの配列で初期化。
    blend = np.zeros_like(imgs[0])
    for img, α in zip(imgs, αs):
        blend += α*img
    return blend

def adjust_imgs(size=(640,526), imgs=[]):
    resized_imgs = []
    for img in imgs:
        resized_imgs.append( cv2.resize(img, size) / 255 )  # float（0~1）に変換する
    return resized_imgs


### 左右反転
# 列を入れ替えることで実現。（スライスが使える）
# https://note.nkmk.me/python-numpy-swap-select/
def turn_vertical(img):
    return img[:, ::-1]



if __name__ == "__main__":
    args = sys.argv
    
    # 画像読み込み
    print(len(args))
    print(args[1])

    image_edit = []
    # 画像を編集
    # トーンカーブ
    if args[1] == 'tc':
        image = cv2.imread(args[2]) / 255  # float（0~1）に変換する
        image_edit = tone_curve(image, 3)
    
    # αブレンディング
    if args[1] == 'a':
        print('αブレンディング を実行します！')
        # 引数：  a 【画像数】 640 480  【img1_path】  【img2_path】  【img3_path】 ... 0.3  0.2  0.5
        img_num = int(args[2])
        size = ( int(args[3]),int(args[4]) )
        imgs = []
        for img_path in args[5:5+img_num]:
            imgs.append( cv2.imread(img_path) )  # float（0~1）に変換する

        imgs = adjust_imgs(size, imgs)

        αs = [float(i) for i in args[ 5+img_num : ]]
        print(αs)

        image_edit = α_blending(imgs, αs)
        print(image_edit)
        if not image_edit.any():
            sys.exit(-1)
    
    # 左右反転
    if args[1] == 'turn':
        image = cv2.imread(args[2]) / 255  # float（0~1）に変換する
        image_edit = turn_vertical(image)

#    print(image)
#    print(image_edit)

    # 画像表示
    preview(image_edit)
    
    #画像保存 imwrite(filename, image)
    cv2.imwrite("result/result_{0}.png".format(args[1]), image_edit*255)





