from flask import Flask, render_template, request
import os
import cv2
from loc_khong_gian import highpass_spatial
from loc_tan_so import highpass_frequency
import webbrowser
import threading

app = Flask(__name__)

INPUT_FOLDER = "static/input"
OUTPUT_FOLDER = "static/output"

@app.route('/')
def index():
    images = os.listdir(INPUT_FOLDER)
    return render_template('index.html', images=images)

@app.route('/process', methods=['POST'])
def process():

    filename = request.form['image']
    path = os.path.join(INPUT_FOLDER, filename)

    spatial = highpass_spatial(path)
    freq = highpass_frequency(path)

    spatial_path = os.path.join(OUTPUT_FOLDER,"spatial_"+filename)
    freq_path = os.path.join(OUTPUT_FOLDER,"freq_"+filename)

    cv2.imwrite(spatial_path, spatial)
    cv2.imwrite(freq_path, freq)

    return render_template('index.html',
                           images=os.listdir(INPUT_FOLDER),
                           original="input/"+filename,
                           spatial="output/spatial_"+filename,
                           freq="output/freq_"+filename)

# 🔥 Tự mở trình duyệt sau khi chạy python app.py
def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == '__main__':
    threading.Timer(1.5, open_browser).start()
    app.run(debug=False)