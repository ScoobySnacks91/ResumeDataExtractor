import os
import json
from PIL import Image
import numpy as np
from colorama import Fore

def convert_bounding_box(bounding_box):
    """Converts bounding box coordinates to [x, y, height, width]."""
    x1, y1, x2, y2 = bounding_box
    x = min(x1, x2)
    y = min(y1, y2)
    width = x2 - x1
    height = y2 - y1
    return [x, y, width, height]

def Ocr_Image_processing(ocr):
    images_folder_path = "data\\images"
    label_studio_task_list = []
    image_files = [f for f in os.listdir(images_folder_path) if f.endswith('.png')]
    total_images = len(image_files)
    
    if total_images == 0:
        print(f"No images found in the specified folder.")
        return
    output_data=[]
    for count, image_file in enumerate(image_files, start=1):
        print(f"Processing image {count}/{total_images}: {image_file}")


        img = Image.open(os.path.join(images_folder_path, image_file))
        img = np.asarray(img)
        image_height, image_width = img.shape[:2]

        result = ocr.ocr(img, cls=False)

        if result is None or not result:
            print(f"No OCR results for image {image_file}")
            continue
        
        for output in result:
            if output is None or not output:
                print(f"No OCR output for image {image_file}")
                continue
            
            for item in output:
                co_ord = item[0]
                text = item[1][0]
                four_co_ord = [co_ord[0][0], co_ord[1][1], co_ord[2][0] - co_ord[0][0], co_ord[2][1] - co_ord[1][1]]
                bbox = {
                    'text':text,
                    'x': 100 * four_co_ord[0] / image_width,
                    'y': 100 * four_co_ord[1] / image_height,
                    'width': 100 * four_co_ord[2] / image_width,
                    'height': 100 * four_co_ord[3] / image_height,
                    'rotation': 0
                }

                if not text:
                    continue
                output_data.append(bbox)
            
        # Print progress
        remaining_images = total_images - count
        print(f"Processed {count} images. {remaining_images} remaining.")

    # Save the results to a JSON file
    with open('data\Image_OCR_output.json', 'w') as f:
        json.dump(output_data, f, indent=4)

    print(f"All images processed. JSON file 'Image_OCR_output.json' created.")


