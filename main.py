from flask import Flask, request, jsonify
import io
import base64
import torch
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration

model_path = "./blip-image-captioning-base"
device = "cuda:0" if torch.cuda.is_available() else "cpu"
processor = AutoProcessor.from_pretrained(model_path, local_files_only=True)
model = BlipForConditionalGeneration.from_pretrained(model_path, local_files_only=True).to(device)

def infer(temp_file):
    img = Image.open(io.BytesIO(temp_file))
    inputs = processor(images=img, text="A picture of", return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=50)
    generation = processor.decode(outputs[0], skip_special_tokens=True)
    return generation

app = Flask(__name__)

@app.route("/", methods=["POST"])
def index():
    content = request.json
    image = base64.b64decode(str(content["image"]))
    text = infer(image)
    return jsonify({
        "text": text
    })

app.run(host="0.0.0.0", port=5000)