import cv2

#画像読み取り
image_path = "sankou" #例えば　"C:\\Users\\admin\\Pictures\\"
image = cv2.imread(image_path+"original.jpg")  #画像読み取り　imread(filename)

#画像表示
cv2.imshow("image",image) #画像出力 imshow(window_name, image)
cv2.waitKey()             #キー入力待ち waitKey(delay=0)
cv2.destroyAllWindows()   #ウィンドウを消す destroyAllWindows()

#画像保存
cv2.imwrite(image_path+"result.jpg",image) #画像保存 imwrite(filename, image)

