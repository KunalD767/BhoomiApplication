import cv2
import numpy as np
import openai
import requests
from PIL import Image
from io import BytesIO
import os
import API

def save_compressed_png(image, output_path, max_size_mb=4):
    compression_level = 9
    while compression_level >= 0:
        cv2.imwrite(output_path, image, [cv2.IMWRITE_PNG_COMPRESSION, compression_level])
        file_size = os.path.getsize(output_path) / (1024 * 1024)
        if file_size <= max_size_mb:
            print(f"Image saved successfully under {max_size_mb} MB with compression level {compression_level}.")
            break
        compression_level -= 1
    if compression_level < 0:
        raise Exception(f"Unable to compress the image to under {max_size_mb} MB.")

sr = cv2.dnn_superres.DnnSuperResImpl_create()

input_path = '/Users/kunal767/Documents/BhoomiApp/SuperResolutionModel/image.jpeg'
img = cv2.imread(input_path)

if img is None:
    raise Exception(f"Failed to load image. Please check the file path: {input_path}")

if img.shape[-1] == 4:
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

model_path = "FSRCNN_x2.pb"
sr.readModel(model_path)
sr.setModel("fsrcnn", 2)

upscaled_img = sr.upsample(img)

sharpen_kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
sharpened_img = cv2.filter2D(upscaled_img, -1, sharpen_kernel)

output_path = 'high_res_sharpened_image.png'
save_compressed_png(sharpened_img, output_path)

with Image.open(output_path) as img_pil:
    rgba_image = img_pil.convert("RGBA")
    rgba_image.save(output_path)

with open(output_path, 'rb') as image_file:
    img_data = image_file.read()

openai.api_key = API.API_KEY

response = openai.Image.create_edit(
    image=img_data,
    prompt="Enhance the clarity and textures of the image, making it more detailed and realistic.",
    n=1,
    size="1024x1024"
)

enhanced_image_url = response['data'][0]['url']
print(f"Enhanced image URL: {enhanced_image_url}")

enhanced_image_response = requests.get(enhanced_image_url)
enhanced_img = Image.open(BytesIO(enhanced_image_response.content))
enhanced_img.save('enhanced_image.png')

print("Enhanced image saved as 'enhanced_image.png'")
