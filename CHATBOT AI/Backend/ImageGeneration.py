import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import load_dotenv
import os
from time import sleep
import sys

# Print Python executable to verify environment
print(sys.executable)
print("Pillow is working!")

# Load environment variables from .env file
env_path = os.path.join("Frontend", ".env")
load_dotenv(env_path)
api_key = os.getenv("HuggingFaceAPIKey")

if not api_key:
    print("API key not found in .env file.")
    exit()

# Define API URL and headers for Hugging Face
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {api_key}"}

# Define image folder path
folder_path = r"Data"
os.makedirs(folder_path, exist_ok=True)

# Function to open and display images
def open_images(prompt):
    prompt = prompt.replace(" ", "_")
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")

# Async function to send image generation requests
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

# Generate and save images
async def generate_images(prompt: str):
    tasks = []
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        filename = f"{prompt.replace(' ', '_')}{i + 1}.jpg"
        with open(os.path.join(folder_path, filename), "wb") as f:
            f.write(image_bytes)

# Wrapper to run the async generation and display the images
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

# Monitor data file for trigger
file_path = r"Frontend\Files\ImageGeneration.data"
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Ensure the file exists
if not os.path.exists(file_path):
    with open(file_path, "w") as f:
        f.write("None|False")

print("Monitoring image generation trigger...")

while True:
    try:
        with open(file_path, "r") as f:
            data: str = f.read().strip()

        if "|" not in data:
            print("Invalid format in ImageGeneration.data, expected 'prompt|True/False'. Waiting...")
            sleep(1)
            continue

        prompt, status = data.split("|", 1)
        prompt = prompt.strip()
        status = status.strip()

        if status == "True":
            print(f"Generating Images for prompt: {prompt}")
            GenerateImages(prompt=prompt)

            # Reset the status to False after generating images
            with open(file_path, "w") as f:
                f.write(f"{prompt}|False")
            break
        else:
            sleep(1)

    except Exception as e:
        print(f"Error: {e}")
        sleep(1)
