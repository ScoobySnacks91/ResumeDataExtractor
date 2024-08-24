import fitz
import os
import shutil

def clear_folder(folder_path):
    """Deletes all files and subdirectories in the given folder."""
    if os.path.exists(folder_path):
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                shutil.rmtree(os.path.join(root, name))
        print(f"Cleared contents of '{folder_path}'.")

def convert_pdfs_to_images(folder_path, images_folder):
    dpi = 300
    zoom = dpi / 72
    magnify = fitz.Matrix(zoom, zoom)

    # Clear the images_folder if it exists
    clear_folder(images_folder)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                
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

def Convert_file_to_images():
    #Call the function
    folder_name = "Input"
    images_folder = "data//images"
    convert_pdfs_to_images(folder_name, images_folder)