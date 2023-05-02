import os
import base64

from paddleocr import PaddleOCR, draw_ocr # PaddleOCR
import cv2 # OpenCV
from opencc import OpenCC # 簡體轉繁體
from PIL import Image, ImageFont, ImageDraw # 影像處理
import numpy as np

# PaddleOCR 目前支持中英文、英文、繁体中文、法語、德語、韓語、日語，可以通過修改 lang 參數進行切換
# 參數依次為 'ch', 'en', 'chinese_cht', 'fr', 'german', 'korean', 'japan
# 參數文件：https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/inference_args.md
paddle_ocr = PaddleOCR(use_angle_cls=True, lang='ch',use_gpu=False, det_limit_side_len=970)

def img_ocr_to_text(file_bytes):
    '''
    對影像進行光學字元辨識處理

    Args:
        - file_bytes: 圖片二進制

    Return:
        - paddle_ocr_result:  paddleOCR 辨識結果    # [[[[]]]]   
        - recognition_word_result: 文字辨識結果 (only 文字)    # ["姓名", "性別"]
        - img_base64: image(二進制, base64)    # "data:image/png;base64 + img_base64"
    '''
    # 讀取圖片檔
    img = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
    # img = cv2.imread(img_path)
    img = __resize_img(img)

    paddle_ocr_result = paddle_ocr.ocr(img, cls=True)
    paddle_ocr_result = paddle_ocr_result[0]

    # 辨識結果清單
    recognition_word_result = []
    # 將簡體中文轉為繁體中文
    cc = OpenCC('s2t')

    for line in paddle_ocr_result:
        # 讀取文字的方框位置
        pt1 = ((int)(line[0][0][0]), (int)(line[0][0][1]))
        pt2 = ((int)(line[0][1][0]), (int)(line[0][1][1]))
        pt3 = ((int)(line[0][2][0]), (int)(line[0][2][1]))
        pt4 = ((int)(line[0][3][0]), (int)(line[0][3][1]))

        # 繪畫方框
        cv2.line(img, pt1, pt2, (0, 0, 255), cv2.LINE_4)
        cv2.line(img, pt2, pt3, (0, 0, 255), cv2.LINE_4)
        cv2.line(img, pt3, pt4, (0, 0, 255), cv2.LINE_4)
        cv2.line(img, pt4, pt1, (0, 0, 255), cv2.LINE_4)

        strText = cc.convert(line[1][0])
        recognition_word_result.append(strText)

        # 繪製中文字
        img = __putText_Chinese(img, strText, (pt1[0], pt1[1]-45), (0, 0, 255), 36)

        # 將處理後的圖片轉換成 base64 編碼的字串
        _, img_encoded = cv2.imencode('.png', img)
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')

    return paddle_ocr_result, recognition_word_result, img_base64

def __resize_img(img):
    '''
    將圖片縮小至螢幕大小

    Args:
        - img: OpenCV 解析後圖片
        - strText: 辨識結果(文字)
        - pos: 文字位置(x, y)
        - color: 文字顏色
        - fontSize: 文字大小
    
    Return:
        縮放後圖片
    '''
    height, width = img.shape[:2]

    # 旋轉圖片
    # if (height > width):
    #     img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # 縮放圖片
    new_width = width
    new_height = height
    if (width > 1080):
        new_width = 1080
        new_height = int((new_width/width) * height)
    if (new_height > 850):
        new_height = 850
        new_width = int((new_height/height) * width)

    resized_img = cv2.resize(img, (new_width, new_height))
    return resized_img

def __putText_Chinese(img, strText, pos, color, fontSize):
    '''
    將辨識結果寫到圖片上

    Args:
        - img: OpenCV 解析後圖片
        - strText: 辨識結果(文字)
        - pos: 文字位置(x, y)
        - color: 文字顏色
        - fontSize: 文字大小
    
    Return:
        更新後圖片 (附上文字)
    '''
    import os

    # 寫入字體
    fontpath = os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../asset/module/simfang.ttf'))
    font = ImageFont.truetype(fontpath, fontSize)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text(pos, strText, font=font, fill=color)
    img = np.array(img_pil)
    return img


if __name__ == '__main__':
    # 讀取圖片檔
    current_dir = os.path.abspath(__file__)
    img_path = os.path.abspath(os.path.join(current_dir, '../../../asset/Certificate.jpg'))
    img = cv2.imread(img_path)

    img = __resize_img(img)

    result = paddle_ocr.ocr(img, cls=True)
    result = result[0]

    # 辨識結果清單
    recognition_word_result = []
    # 將簡體中文轉為繁體中文
    cc = OpenCC('s2t')

    print(result)

    for line in result:
        print('-----------------------------')
        print(line)

        # 讀取文字的方框位置
        pt1 = ((int)(line[0][0][0]), (int)(line[0][0][1]))
        pt2 = ((int)(line[0][1][0]), (int)(line[0][1][1]))
        pt3 = ((int)(line[0][2][0]), (int)(line[0][2][1]))
        pt4 = ((int)(line[0][3][0]), (int)(line[0][3][1]))

        # 繪畫方框
        cv2.line(img, pt1, pt2, (0, 0, 255), cv2.LINE_4)
        cv2.line(img, pt2, pt3, (0, 0, 255), cv2.LINE_4)
        cv2.line(img, pt3, pt4, (0, 0, 255), cv2.LINE_4)
        cv2.line(img, pt4, pt1, (0, 0, 255), cv2.LINE_4)

        strText = cc.convert(line[1][0])
        recognition_word_result.append(strText)

        # 繪製中文字
        img = __putText_Chinese(img, strText, (pt1[0], pt1[1]-45), (0, 0, 255), 36)
    
    cv2.imshow("OCR_Result", img)
    cv2.waitKey()
    cv2.destroyAllWindows
    print()
    print(recognition_word_result)
    print()

    # for idx in range(len(result)):
    #     res = result[idx]
    #     for line in res:
    #         print(line)

    # result = result[0]
    # image = Image.open(img_path).convert('RGB')
    # boxes = [line[0] for line in result]
    # txts = [line[1][0] for line in result]
    # scores = [line[1][1] for line in result]
    # im_show = draw_ocr(image, boxes, txts, scores, font_path='./word_type/simfang.ttf')
    # im_show = Image.fromarray(im_show)
    # im_show.show()

    # im_show.save('result.jpg')