from PIL import Image
import shutil
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()

root_dir = os.path.dirname(find_dotenv())

ASCII_CHARS = ['@', '#', '*', '?',  '|', '.', ' ']
#ASCII_CHARS = ['.', ' ']

# Resize image while maintaining aspect ratio
def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)
    return image.resize((new_width, new_height))

# Main function to convert image to ASCII
def image_to_ascii(image_path, new_width=100):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image file: {e}")
        return

    image = resize_image(image, new_width)
    image = image.convert("L")
    pixels = image.getdata()
    ascii_str = ''.join([ASCII_CHARS[pixel * (len(ASCII_CHARS) - 1) // 255] for pixel in pixels])

    img_width = image.width
    ascii_img = "\n".join([ascii_str[i:i+img_width] for i in range(0, len(ascii_str), img_width)])

    return ascii_img

def ascii_converter(output_path):
    folder_path = os.path.join(root_dir, os.getenv("Folder_path"))
    archive_path = os.path.join(root_dir, os.getenv("Archive_path"))
    no_img_flag = True
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            img_path = os.path.join(folder_path, filename)
            no_img_flag = False
            try:
                ascii_art = image_to_ascii(img_path, new_width=100)
                if ascii_art:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    name, ext = os.path.splitext(filename)
                    final_file_name = name + "_" + timestamp + ext
                    with open(f"{output_path}\\{final_file_name}.txt", "w") as f:
                        f.write(ascii_art)
                    dst_name = name + "_" + timestamp + ext
                    dst_path = os.path.join(archive_path, dst_name)
                    shutil.move(img_path, dst_path)
                    print(f"{filename} image got converted succssfully")
            except Exception as ex:
                print(f"Failed to convert '{img_path}' to ASCII due to: ", ex)
    if no_img_flag:
        print("No Images found.. exiting")
