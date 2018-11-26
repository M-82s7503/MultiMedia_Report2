from PIL import Image
import numpy as np

# 元となる画像の読み込み
img = Image.open('original.jpg')
#オリジナル画像の幅と高さを取得
width, height = img.size
print("width, height = ", width, "," ,height)
# オリジナル画像と同じサイズのImageオブジェクトを作成する
img2 = Image.new('RGB', (width, height))

img_pixels = []
for y in range(height):
  for x in range(width):
    # getpixel((x,y))で左からx番目,上からy番目のピクセルの色を取得し、img_pixelsに追加する
    img_pixels.append(img.getpixel((x,y)))
# あとで計算しやすいようにnumpyのarrayに変換しておく
img_pixels = np.array(img_pixels)
print(img_pixels)


img_pixels[100][200]
# => array([255,255,255])


img2.putpixel((100, 200), (0, 0, 255))


img2.show()

img2.save('edited_img.jpg')
