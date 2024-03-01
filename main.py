import json
from PIL import Image
import requests
from io import BytesIO
import streamlit as st
import google.generativeai as gen_ai

st.set_page_config(
    page_title="Image Captions",
    page_icon="📷",
    layout="centered",
)

config_data = json.load(open("config.json"))
GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]

gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro-vision')

def get_image_caption(prompt, image, model=model):
    response = model.generate_content([prompt, image])
    image_caption = response.text
    return image_caption

st.title("📷 Snap Narrate")

image_source = st.radio("Select Image Source:", ("Upload an image", "Enter Image URL"))

if image_source == "Upload an image":
    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
else:
    image_url = st.text_input("Enter Image URL:")
    if st.button("Generate Caption"):
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
        except Exception as e:
            st.error(f"Error downloading the image from the provided URL: {str(e)}")
            st.stop()
            
        col1, col2 = st.columns(2)
        with col1:
            resized_img = image.resize((800, 500))
            st.image(resized_img)

        default_prompt = "write a short caption for this image"
        caption = get_image_caption(default_prompt, image)
        with col2:
            st.info(caption)
