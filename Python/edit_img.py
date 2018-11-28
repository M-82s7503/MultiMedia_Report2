import sys
import cv2
from PIL import Image, ImageDraw
import random
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

### αブレンディング 図4.21
def α_blending(imgs=[], αs=[]):
    # or sum(αs) != 1
    if len(imgs) < 2 or len(imgs) != len(αs):
        return []  # ほんとはエラー処理すべき

    # 0埋めの配列で初期化。
    blend = np.zeros_like(imgs[0])
    for img, α in zip(imgs, αs):
        blend += α*img
    return blend

### αブレンディング 図4.22
# direct： 境界線の方向。 縦方向→0, 横方向→1
def α_blending_22(img1, img2, direct):
    # img1 のサイズに合わせる。
    size = (img1.shape[1], img1.shape[0])
    imgs = adjust_imgs(size, [img1, img2])
    img1, img2 = imgs[0], imgs[1]
    print(img1.shape, img2.shape)
    # 0埋めの配列で初期化。
    blend = np.zeros_like(img1)
    α = div_α = 1/size[direct]
    for i in range(size[direct]):
        # 列（または行）を取り出して、αをかける。
        if direct == 0:
            blend[:,i] += α*img2[:,i] + (1-α)*img1[:,i]
        else:
            blend[i,:] += α*img2[i,:] + (1-α)*img1[i,:]
        α += div_α
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

### 5秒ごとにタイル回転？
# 3x3 タイルをランダムに t_num 個選んで、左右反転させる。
def turn_rand3x3(img, t_num, x_div3, y_div3):
    for count in range(t_num):
        # 回転させるタイルの中心座標を算出
        p = ( 3* random.randint(0, x_div3),  3* random.randint(0,y_div3) )
        # 左右反転した 3x3 データを、元データに代入
        img[p[0]-1:p[0]+1, p[1]-1:p[1]+1] = turn_vertical(img[p[0]-1:p[0]+1, p[1]-1:p[1]+1])
    return img



if __name__ == "__main__":
    # コマンドライン引数で、どれを実行するかを指定する。
    args = sys.argv
    
    image_edit = []  # 処理結果画像
    # 画像を編集
    # トーンカーブ
    '''
    引数：  tc 【γ値】 【img_path】
    '''
    if args[1] == 'tc':
        γ = float(args[2])
        image = cv2.imread(args[3]) / 255  # float（0~1）に変換する
        image_edit = tone_curve(image, γ)
    
    # αブレンディング（複数枚対応ver）
    '''
    引数：  
      a 【画像数】 640 480 【img1_path】 【img2_path】 【img3_path】... 0.3  0.2  0.5 ...
    '''
    if args[1] == 'a':
        img_num = int(args[2])
        size = ( int(args[3]),int(args[4]) )
        imgs = []
        for img_path in args[5:5+img_num]:
            imgs.append( cv2.imread(img_path) )  # float（0~1）に変換する

        imgs = adjust_imgs(size, imgs)
        αs = [float(i) for i in args[ 5+img_num : ]]

        image_edit = α_blending(imgs, αs)
        if not image_edit.any():
            sys.exit(-1)
    
    # αブレンディング（教科書 図4.22 ver）
    '''
    引数：  
      a 【画像数】 640 480 【img1_path】 【img2_path】 【img3_path】... 0.3  0.2  0.5 ...
    '''
    if args[1] == 'a2':
        image1 = cv2.imread(args[2])  # float（0~1）に変換する
        image2 = cv2.imread(args[3])  # float（0~1）に変換する
        image_edit = α_blending_22(image1, image2, int(args[4]))

    # 左右反転
    '''
    引数：  turn 【img_path】
    '''
    if args[1] == 't':
        image = cv2.imread(args[2]) / 255  # float（0~1）に変換する
        image_edit = turn_vertical(image)

    # 5秒ごとにタイル回転？
    '''
    引数：  t_tile 【img_path】
    '''
    if args[1] == 'tt':
        image = cv2.imread(args[2]) / 255
        # 各種パラメータをセット
        im_size = ( image.shape[0]/3 ) * ( image.shape[1]/3 )
        t_num = int(im_size / 10)  # 10回で全部反転できるようにする。
        div_num = int( im_size *1.2 / t_num )  # （ランダムなので）12回くらい？

        x_div3, y_div3 = int(image.shape[0]/3), int(image.shape[1]/3)
        # 個別に保存
        for i in range(div_num):
            cv2.imwrite("result/anime_imgs/{0}.png".format(i), image*255)
            image = turn_rand3x3(image, t_num, x_div3, y_div3)
        """
        # 保存した画像をアニメにする。
        imgs = []
        for i in range(div_num):
            imgs.append( Image.open( 'result/anime_imgs/{0}.png'.format(i) ) )
        imgs[0].save('result/turn_tile_anime.gif',
               save_all=True, append_images=imgs[1:], optimize=False, duration=1000)
        """
        sys.exit(0)


    # 画像表示
    preview(image_edit)
    
    #画像保存 imwrite(filename, image)
    cv2.imwrite("result/result_{0}.png".format(args[1]), image_edit*255)





