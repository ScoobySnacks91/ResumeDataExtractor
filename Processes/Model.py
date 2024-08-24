import numpy as np
import pickle
import json
import regex as re

def custom_model(model):
    def isdate(text):
        # Year pattern for years after 1950
        year_pattern_after_1950 = r'\b(19[5-9][1-9]|19[6-9][0-9]|20[0-9]{2}|2100)\b'
    
        # Search for the pattern in the text
        if re.search(year_pattern_after_1950, text):           
            return True
        else:
           return False

    # Load training data (to get the actual labels)
    with open(r'data\Encoded_Data.pkl', 'rb') as file:
        data = pickle.load(file)

    # Initialize lists to store predictions and corresponding actual labels
    predicted_labels = []

    predicted_label = 0  # Initial predicted label

    # Iterate over each time step in the selected sequence
    print("Start predictions")
    for time_step in data:
        # Insert the predicted label at the beginning of the time_step
        x_predict = np.insert(time_step, 0, predicted_label)
    
        # Reshape x_predict to (1, input_features_length, 1)
        x_predict = np.expand_dims(x_predict, axis=-1)  # Shape: (32, 1)
        x_predict = np.expand_dims(x_predict, axis=0)   # Shape: (1, 32, 1)
    
        # Make prediction
        prediction = model.predict(x_predict,verbose=0)
    
        # Get the predicted label
        predicted_label = np.argmax(prediction, axis=-1)[0]
    
        # Append the predicted and actual labels to the lists
        predicted_labels.append(predicted_label)
    print("predictions ended")

    with open(r"data\Image_OCR_output.json", 'r',encoding='utf-8') as file:
        data_text=json.load(file)

    text=[]

    l_label=0
    ll_label=0
    for texts,label in zip(data_text,predicted_labels):    
        if label==1:
            text.append(texts['text'])
        elif l_label==1   and isdate(texts['text']):
            text.append(texts['text'])

        ll_label=l_label
        l_label=label

    with open(r"data\text.txt", 'w',encoding='utf-8') as file:
        for tex in text:
            file.write(tex + "\n")  # Add a newline character to separate lines
        print("Text file Created")