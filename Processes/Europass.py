import json

def IsEuropass():
    #Getting Data from json file
    with open(r"data\Image_OCR_output.json", 'r') as file:
        data=json.load(file)

    IsEuropass=False
    texts=[]
    for set in data:
        texts.append(set['text'])
        if set['text']=='europass':
            IsEuropass=True

    workExperience=[]
    we=False
    wee=True
    for text in texts:
        if text=='WORK EXPERIENCE':
            we=True
            if we:
                if 'EDUCATION AND' in text or 'HOBBIES' in text or 'LANGUAGE SKILLS' in text or 'DRIVING LICENCE' in text or 'DIGITAL SKILLS' in text or 'COMMUNICATION AND' in text or 'HONORS' in text or 'SKILLS' in text or 'RECOMMENDATIONS' in text:
                    wee=False
        if we and wee:
            workExperience.append(text)
    print(IsEuropass)

    with open(r"data\text.txt", 'w',encoding='utf-8') as file:
      for tex in workExperience:
         file.write(tex + "\n")  # Add a newline character to separate lines
      print("Text file Created")

    with open(r"data\isEuropass.txt", 'w',encoding='utf-8') as file:
        if IsEuropass:
           file.write("yes")  # Add a newline character to separate lines
        else:
            file.write("no")
