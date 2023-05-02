import cv2
import numpy as np
from PIL import Image
import pytesseract
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# if (height > width):
#     dim_size = (int(width * 900 / height), 900)
# else:
#     dim_size = (900, int(height * 900 / width))
# img = cv2.resize(img, dim_size, interpolation=cv2.INTER_AREA)
# 提升對比度
# alpha = 1.1
# beta = 0
# adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

def change_image_old(imagePath):
    img = cv2.imread(imagePath, cv2.IMREAD_COLOR)

    pil_image = Image.fromarray(np.uint8(img))
    img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2RGBA)
    height, width = img.shape[:2]

    if (height > width):
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        # img = cv2.flip(img, 1)

    # 提升對比度
    alpha = 2
    beta = 0
    adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    # 轉化成灰度圖
    gray = cv2.cvtColor(adjusted, cv2.COLOR_BGR2GRAY)

    cv2.imshow('My Image', gray)

    # 按下任意鍵則關閉所有視窗
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    convert = gray
    return convert

def change_image(imagePath):
    # 1. 讀取圖片
    img = cv2.imread(imagePath, cv2.IMREAD_COLOR)

    height, width = img.shape[:2]

    if (height > width):
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        # img = cv2.flip(img, 1)

    # 2. 提升對比度
    alpha = 2
    beta = 0
    adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    # 3. 轉化成灰度圖
    gray = cv2.cvtColor(adjusted, cv2.COLOR_BGR2GRAY)

    # 4. 將圖片做模糊化，可以降噪
    # blur_img = cv2.blur(gray, (3, 3))
    # blur_img = cv2.GaussianBlur(gray, (5, 5), 0)
    blur_img = cv2.medianBlur(gray, 3)

    # # 4.影像去噪
    # gray = cv2.fastNlMeansDenoisingColored(img, None, 10, 3, 3, 3)
    cv2.imshow('My Image', blur_img)

    # 按下任意鍵則關閉所有視窗
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    # 5. 二質化
    # 一般圖二值化
    # binary_img = cv2.threshold(blur_img, 120, 255, cv2.THRESH_BINARY)[1]
    # 一般圖算術平均法的自適應二值化(有模糊降噪)
    binary_img = cv2.adaptiveThreshold(blur_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    # 一般圖高斯加權均值法自適應二值化
    # binary_img = cv2.adaptiveThreshold(blur_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 10)

    # 6. 腐蝕
    kernel = np.ones((2, 2), np.uint8)
    for i in range(5):
        ero_img = cv2.erode(binary_img, kernel, iterations=1)
    # 7. 膨脹
    for i in range(5):
        dil_img = cv2.dilate(ero_img, kernel, iterations=1)
    # 8. 開運算
    # open_img = cv2.morphologyEx(dil_img, cv2.MORPH_OPEN, kernel)
    # 9. 閉運算
    # close_img = cv2.morphologyEx(open_img, cv2.MORPH_CLOSE, kernel)

    
    cv2.imshow('My Image', dil_img)

    # 按下任意鍵則關閉所有視窗
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return dil_img

def revise_image(imgPath):
    #1.讀取影像
    img = cv2.imread(imagePath, cv2.IMREAD_COLOR)

    # 2. 調整圖像大小
    img = cv2.resize(img, (428, 270), interpolation=cv2.INTER_CUBIC)

    # 3.影像去噪
    gray = cv2.fastNlMeansDenoisingColored(img, None, 10, 3, 3, 3)
    coefficients = [0, 1, 1]
    m = np.array(coefficients).reshape((1, 3))

    #旋轉圖片
    # gray = cv2.transform(gray, m)

    #4.閾值 180  maxval:255
    ret, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    ele = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 10))

    #5.膨脹操作
    dilation = cv2.dilate(binary, ele, iterations=1)

    cv2.imshow('My Image', dilation)

    # 按下任意鍵則關閉所有視窗
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # i_index = 0
    # #6.尋找與身份證字號相似的大小輪廓(contours)
    # image, contours = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # for box in contours:  
    #         i_index+=1
    #         h = abs(box[0][1] - box[2][1])
    #         w = abs(box[0][0] - box[2][0])
    #         max_point=box[3][0]
    #         Xs = [i[0] for i in box]
    #         Ys = [i[1] for i in box]
    #         x1 = min(Xs)
    #         y1 = min(Ys)
    #         #找到的輪廓用緣色的框畫出來
    #         cv2.drawContours(img, [box], 0, (0, 255, 0), 2)
    #         img_gray=img[y1:y1 + h, x1:x1+w]
    #         # 取得每一個小輪廓二值化圖片
    #         idImg = cv2.resize(img_gray, (img_gray.shape[1] * 3, img_gray.shape[0] * 3), interpolation=cv2.INTER_CUBIC)
    #         idImg = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    #         #otsu二值化操作
    #         retval, idImg = cv2.threshold(idImg , 120, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
            
    #         print("index:",str(i_index),"tag:",box,"high:",h,"width:",w)
    #         #抓到哪些輪廓
    #         cv2.imwrite("data\idImg_"+str(i_index)+".png", idImg)
    #         cv2.imwrite("data\contours.png", img)    
    #         #x軸在最右邊，且輪廓大於4倍視為身份證字號位置
    #         if (max_point>max_item and w//h>=4.0):
    #             max_item=max_point
    #             max_index=i_index

    idImg = dilation

    #圖片存在
    if(idImg is not None):
            image = Image.fromarray(idImg)
            result = pytesseract.image_to_string(image, lang="chi_tra+eng")
            if(result==""):
                print("don't know")
            else:
                print('the detect result is '+result)
            f, axarr = plt.subplots(2, 3)
            #open cv讀照片
            axarr[0, 0].imshow(cv2.imread(imgPath))
            # axarr[0, 1].imshow(cv2.imread("data\gray.png"))
            # axarr[0, 2].imshow(cv2.imread("data/binary.png"))
            # axarr[1, 0].imshow(cv2.imread("data\dilation.png"))
            # axarr[1, 1].imshow(cv2.imread("data\contours.png"))
            # axarr[1, 2].imshow(cv2.imread("data\idImg_"+str(2)+".png"))
            plt.show()
    else:
        print('not found id')
# =============================================================================
if __name__ == '__main__':
    # 读取文件
    imagePath = r"./asset/hamastar.jpg"

    # img = change_image_old(imagePath)
    img = change_image(imagePath)
    # img = revise_image(imagePath)

    scantext = pytesseract.image_to_string(img, lang='chi_tra+eng')
    print("-- 輸出 ---")
    print(scantext)
