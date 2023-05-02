## 伺服器執行
#### 正常執行方法 ( 官方推薦 )
> #### set FLASK_APP=app.py
> #### flask run
>> #### flask run --reload --debugger --host 0.0.0.0 --port 5000
>> - reload # 修改 py 檔後，Flask server 會自動 reload
>> - debugger # 如果有錯誤，會在頁面上顯示是哪一行錯誤
>> - host # 可以指定允許訪問的主機IP，0.0.0.0 為所有主機的意思
>> - port # 自訂網路埠號的參數
> ###### <br/>
<br/>

#### 以 python 執行
> #### set FLASK_APP=app.py
> #### python -m flask run
<br/>

#### 直接執行 app.py (不推薦)
> #### python app.py
<br/>

------
## 檔案擺放架構
```
.
├─ asset    # 圖檔、資源
├─ controllers  # 控制器
│   └─ img_ocr_controller.py   # 光學字元辨識控制器
│
├─ models   # 模型
│   └─ logic    # 邏輯層
|       ├─ image_ocr_logic.py   # 光學字元辨識邏輯
|       └─ text_classfify_logic.py  # 文字分類邏輯
|
├─ static   # 靜態屬性
|   └─ css  # css檔案
|       └─ upload_img.css   # 圖像文字辨識頁面CSS
|
├─ templates    # 頁面
|   └─ upload_img.html  # 圖像文字辨識頁面
|
├─ text_file    # 一些沒有用到的重要檔案
├─ view    # 視圖
├─ app.py   # 主執行程式
└─ README.md    # 說明文件
```

<br/>

------
## templates 畫面
- upload_img.html # 圖片上傳及辨識頁面

<br/>

------
## API 串接格式
| POST        |將圖片進行光學字元辨識                         |
|-------------|---------------------------------------------|
|HTTP Method  |POST                                         |
|Resource     |{HostURL}/ocr/image                          |
|Request Body |圖片二進制 byte <br> image_file：FormData       |
|Response Body|辨識文字結果及圖片結果 <br> { <br> ocr_classify_result：{"辨識結果配對"}, <br> ocr_word_result：["辨識文字結果"], <br> img：img (base64) <br> }|
```json
POST {HostURL}/ocr/image
request: {
    "image_file": "FormData"
}
responses: {
    "ocr_classify_result" {"姓名":"XXX"},
    "ocr_word_result：": ["姓名", "性別"],
    "img": "data:image/png;base64 + img_base64"
}
```