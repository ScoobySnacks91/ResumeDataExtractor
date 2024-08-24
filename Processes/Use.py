import numpy as np
import json
import pickle

def Use(model):
    # Example usage: encoding sentences
    def encode_sentence(sentence):
        embeddings = model(sentence)
        return embeddings

    #Getting Data from json file
    with open(r"data\Image_OCR_output.json", 'r') as file:
      data=json.load(file)

    texts=[]
    for set in data:
     texts.append(set['text'])

    embenddings=encode_sentence(texts)
    i=0
    Encoded_Data=[]
    for set,emb in zip(data,embenddings):
        coord=[set['x'],set['y'],set['width'],set['height'],set['rotation']]
        spatial=[i]+coord
        combined_features = np.concatenate([spatial,emb])
        Encoded_Data.append(combined_features)
        # print(i)
        i=i+1

    with open(r'data\Encoded_Data.pkl', 'wb') as file:
        pickle.dump(Encoded_Data, file)
        print("Encoded_Data.pkl created succesfully")

