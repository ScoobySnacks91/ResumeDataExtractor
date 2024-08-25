from colorama import Fore
import time
from paddleocr import PaddleOCR
import tensorflow_hub as hub
import os
import tensorflow as tf
import spacy

#Initialize all models
#===================================================================================================================================
# Initialize OCR engine
ocr = PaddleOCR(use_angle_cls=False, lang='en', rec=False)

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Path where the model files are stored
Use_model_path=r"C:\Users\User\.cache\kagglehub\models\google\universal-sentence-encoder\tensorFlow2\universal-sentence-encoder\2"

# Load the Universal Sentence Encoder model
Use_model = hub.load(Use_model_path)

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Load the trained model
model = tf.keras.models.load_model(r'Processes\my_trained_model4.h5')

# Load spaCy model
nlp = spacy.load("en_core_web_md")
#===================================================================================================================================

def ProcessResume():
    start_time = time.time()
    # Run the functions
    print(Fore.CYAN+"\nConverting files to images")
    print("==================================================================================================================")
    from Processes.File_Manager import convert_file_to_images
    file_in_input=convert_file_to_images()
    if(file_in_input==0):
        print(Fore.RED+"Input folder is empty or file is of wrong type!!!")
        print(Fore.CYAN+"==================================================================================================================")
    else:
        print(Fore.CYAN+"==================================================================================================================")
        print(Fore.MAGENTA+"Processing OCR Images")
        print("==================================================================================================================")

        from Processes.Image_OCR import Ocr_Image_processing
        Ocr_Image_processing(ocr)
        print("==================================================================================================================")

        print(Fore.BLUE+"Checking if its Europass")
        print("==================================================================================================================")

        from Processes.Europass import IsEuropass
        IsEuropass()

        # Open the file in read mode
        with open('data\\isEuropass.txt', 'r') as file:
            first_line = file.readline().strip().lower()
    
        # Convert the first line to 1 or 0
        isEuropass = 1 if first_line == "yes" else 0 if first_line == "no" else None
        print("==================================================================================================================")
        if isEuropass == 0:
            print(Fore.YELLOW+"USE encoding")
            print("==================================================================================================================")

            from Processes.Use import Use
            Use(Use_model)
            print("==================================================================================================================")

            print(Fore.GREEN+"Classifying data as experience")
            print("==================================================================================================================")
            from Processes.Model import custom_model
            custom_model(model)
            print("==================================================================================================================")

        print(Fore.LIGHTBLACK_EX+"Structuring Data:")   
        print("==================================================================================================================")
        from Processes.Data_Structuring import DataSrtucturing
        DataSrtucturing(spacy,nlp)
        print("==================================================================================================================")
    

    end_time = time.time()
    execution_time = end_time - start_time
    #print(f"Execution time: {execution_time} seconds")

ProcessResume()

# # Simulate message receiving function (this could be replaced with your actual message receiving logic)
# def get_message():
#     # For the sake of example, this function returns None (no message) or a random message.
#     # Replace this with actual code to fetch messages from your external source (e.g., API, socket, etc.)
#     return None  # Or return a message when available.


# while True:
#     # Check if a message is available
#     message = get_message()

#     # If a message is received, handle it
#     if message:
#         ProcessResume()
    
#     # Wait for a short period to avoid busy-waiting
#     time.sleep(1)  # Adjust the delay as needed (e.g., 1 second)