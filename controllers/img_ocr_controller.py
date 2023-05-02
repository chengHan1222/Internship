from flask import jsonify, request, abort
from werkzeug.exceptions import HTTPException

from models.logic.image_ocr_logic import img_ocr_to_text
from models.logic.text_classify_logic import text_classify_logic


def init_app(app):
    @app.route('/ocr/image', methods=['POST'])
    def img_ocr():
        try:
            file = request.files['image_file']
        except HTTPException as e:
            return abort(e.code, e.description)

        try:
            if file.filename != '':
                # 將文件對象轉換為字節流
                file_bytes = file.read()

                # PaddleOCR 辨識
                ocr_result, ocr_word_result, img_base64 = img_ocr_to_text(file_bytes)

                # 辨識結果分類
                ocr_classify_result = text_classify_logic(ocr_result)

                return jsonify(ocr_classify_result=ocr_classify_result, ocr_word_result=ocr_word_result, img='data:image/png;base64,' + img_base64)
            return ''
        except Exception as e:
            print('Caught this error: ' + repr(e))
            return abort(e.code, e.description)
