import re
import pandas as pd
import math
import openpyxl
import os
import shutil

def DataSrtucturing(spacy,nlp):
    # Read the text file
    with open("data\\text.txt", "r") as file:
        text = file.read()

    # Define the keywords to search for
    keywords = [
        "Work Experience", "Job Experience", "Experience", "Professional Experience",    
        "Work History", "Job History", "Career History", "Employment History", "Experience","Employement History","Employement history","Employment Chronicle"
    ]

    
    # Function to capitalize and lowercase each keyword
    def transform_keywords(keywords):
        transformed_keywords = []
        for keyword in keywords:
            transformed_keywords.append(keyword.upper())  # Add the keyword in uppercase
            transformed_keywords.append(keyword.lower())  # Add the keyword in lowercase
        return transformed_keywords
    
    # Transform the keywords
    transformed_keywords = transform_keywords(keywords)

    # Combine the original and transformed lists
    combined_keywords = keywords + transformed_keywords

    # Find the position of the first keyword found in the text
    position = None
    for keyword in combined_keywords:
        pos = text.find(keyword)
        if pos != -1:
            position = pos
            break

    # If a keyword is found, keep everything from the position of the keyword onwards
    if position is not None:
        text = text[position:]

    # Process the text with spaCy
    doc = nlp(text)

    # Initialize lists to store results
    organizations = []
    gpe_entities = []
    dates = []
    years_of_experience = []

    # Extract entities using spaCy
    for ent in doc.ents:
        if ent.label_ == "ORG":
            organizations.append(ent.text)
        elif ent.label_ == "GPE":
            gpe_entities.append(ent.text)

    # Combined regex pattern for 4-digit numbers and specific words
    combined_pattern = r'\b(\d{4})\b|\b(Present|Current|CURRENT|current|Now|till date|stil working)\b'
    combined_regex = re.compile(combined_pattern, re.IGNORECASE)

    # Use combined regex pattern to find all matches
    matches = combined_regex.findall(text)

    # Process matches to separate dates and specific words
    for match in matches:
        if match[0]:  # This corresponds to a 4-digit number
            dates.append(match[0])
        elif match[1]:  # This corresponds to a specific word
            dates.append(match[1])

    # Regex pattern for years of experience
    experience_pattern = re.compile(r'\b(\d+\.?\d*)\s*(year|years|Year|Years)\b', re.IGNORECASE)

    # Use regex to find all years of experience phrases
    experience_matches = experience_pattern.findall(text)

    # Process experience matches to format them correctly
    for match in experience_matches:
        number = match[0]
        unit = match[1].lower()
        if unit == 'year':
            years_of_experience.append(f'{number} Year')
        else:
            years_of_experience.append(f'{number} Years')
    #===================================================================================
    def is_number(s):
        """Check if the string can be converted to a number."""
        try:
            float(s)  # We use float to handle numbers with decimal points as well.
            return True
        except ValueError:
            return False
    
    threshold=1970

    # Filter and convert to numbers
    filtered_dates=[]
    for i in range(len(dates)):
        if is_number(dates[i]):
            if float(dates[i])>threshold:
                filtered_dates.append(dates[i])
        if is_number(dates[i] !=1):
            filtered_dates.append(dates[i])
    #==================================================================================
    start_date=[]
    end_date=[]

    i=0
    while i<math.floor(len(dates)/2):
        start_date.append(dates[2*i])
        end_date.append(dates[2*i+1])
        i=i+1
    #========================================================================================
    #Role
    #========================================================================================
    # Load the Excel file
    Professions_file_path = "data\\Professions.xlsx"  # Adjust the file path if necessary
    df = pd.read_excel(Professions_file_path, sheet_name='Sheet1')  # Update the file and sheet name as needed

    # Extract the list of words from the column
    words_to_find = df['Words'].dropna().tolist()

    # Create the regex pattern from the list
    pattern = r'\b(?:' + '|'.join(words_to_find) + r')\b'
    # Set to store unique common words

    # Find all matches
    matches_Role = re.findall(pattern, text, flags=re.IGNORECASE)

    #=========================================================================================
    # Create a DataFrame
    df = pd.DataFrame({
        'Key':pd.Series(),
        'Role':pd.Series(matches_Role),
        'Company (Organisation)': pd.Series(organizations),
        'Location (GPE)': pd.Series(gpe_entities),
        'Start_Date': pd.Series(start_date),
        'End_Date':pd.Series(end_date),
        'Responsibilities':pd.Series(),
        'Years of Experience': pd.Series(years_of_experience)})
    #=======================================================================================
    def create_or_replace_directory(dir_path):
        # If the directory exists, remove it
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
    
        # Create the new directory
        os.makedirs(dir_path)
        print(f"Directory '{dir_path}' created or replaced.")

    dir_name = "Output"
    create_or_replace_directory(dir_name)

    # Export to Excel
    df.to_excel("Output\\output.xlsx", index=False, engine='openpyxl')
    print("Output.xlsx file created!")