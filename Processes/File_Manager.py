import fitz
import os
import shutil
from PIL import Image

def convert_file_to_images():
    def clear_folder(folder_path):
        """Deletes all files and subdirectories in the given folder."""
        if os.path.exists(folder_path):
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    shutil.rmtree(os.path.join(root, name))
            print(f"Cleared contents of '{folder_path}'.")

    def is_image(file_path):
        """Checks if a given file is an image by trying to open it with PIL."""
        try:
            Image.open(file_path)
            return True
        except IOError:
            return False

    def move_image_to_folder(image_path, images_folder):
        """Moves an image to the images folder."""
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
            print(f"Created '{images_folder}' directory.")
        
        # Move the image
        shutil.move(image_path, images_folder)
        print(f"Moved image: {image_path} to {images_folder}")

    def convert_pdfs_to_images(folder_path, images_folder):
        dpi = 300
        zoom = dpi / 72
        magnify = fitz.Matrix(zoom, zoom)

        # Clear the images_folder if it exists
        clear_folder(images_folder)

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Check if it's an image and move it directly if it is
                if is_image(file_path):
                    move_image_to_folder(file_path, images_folder)
                # Otherwise, if it's a PDF, convert it to images
                elif file.lower().endswith('.pdf'):
                    pdf_path = file_path
                    
                    try:
                        doc = fitz.open(pdf_path)
                        print(f"Successfully opened {pdf_path}")
                    except Exception as e:
                        print(f"Error opening {pdf_path}: {e}")
                        continue
                    
                    count = 0

                    if not os.path.exists(images_folder):
                        os.makedirs(images_folder)
                        print(f"Created '{images_folder}' directory.")

                    for page in doc:
                        count += 1
                        pix = page.get_pixmap(matrix=magnify)
                        image_path = os.path.join(images_folder, f"{os.path.splitext(file)[0]}_page_{count}.png")
                        pix.save(image_path)
                        print(f"Saved image: {image_path}")

    #Clear the ouput Folder
    clear_folder("Output")
    # Define the paths
    folder_name = "Input"
    images_folder = "data//images"
    
    # Check if the Input folder exists and is not empty
    if not os.path.exists(folder_name) or not os.listdir(folder_name):  # Check if the folder doesn't exist or is empty
        return 0
    
    # Clear the 'data' folder before doing anything
    data_folder = "data"
    clear_folder(data_folder)
    
    # Call the function to convert PDFs to images and move existing images
    convert_pdfs_to_images(folder_name, images_folder)
    
    # After processing, check if the images folder exists and has any images
    if not os.path.exists(images_folder) or not os.listdir(images_folder):
        return 0  # Return 0 if the folder doesn't exist or is empty
    
    return 1  # Return 1 if processing is successful
