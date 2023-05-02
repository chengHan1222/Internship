from flask import Flask, render_template
import controllers.img_ocr_controller as img_ocr_controller

app = Flask(__name__)
CONFIGS = {
    "ENV": "development",
    "DEBUG": True
}
app.config.from_object(CONFIGS)

# 光學字元辨識 API
img_ocr_controller.init_app(app)


@app.route('/')
def index(): 
    return render_template('upload_img.html', text="")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)