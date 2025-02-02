"""
Take input as image from web app and return the image with bounding box and image classs 
"""
import argparse
import io
import os
from PIL import Image
import datetime

import torch
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S-%f"


@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if not file:
            return

        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        results = model([img])

        results.render()  # updates results.imgs with boxes and labels
        now_time = datetime.datetime.now().strftime(DATETIME_FORMAT)
        img_savename = f"static/{now_time}.png"
        Image.fromarray(results.ims[0]).save(img_savename)
        return redirect(img_savename)

    return render_template("myapp.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()


    #model = torch.hub.load('ultralytics/yolov5', 'custom',path= "yolov5-master/runs/train/exp3/weights/best.pt", force_reload=True)
    model = torch.hub.load('ultralytics/yolov5', 'custom', path="yolov5-master/runs/train/exp3/weights/best.pt", force_reload=True)

    model.eval()
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat

