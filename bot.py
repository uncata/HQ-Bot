from bs4 import BeautifulSoup
from PIL import Image, ImageEnhance
import lxml
import pytesseract
import requests
import time

# Use this line if pytesseract not in PATH environment 
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

# Process image to make image easier to read for pytesseract
def processImage(img):
    # Increase contrast 
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(2)

    # Increase sharpness
    sharper = ImageEnhance.Sharpness(img)
    img = sharper.enhance(2)

    # Increase brightness
    brighter = ImageEnhance.Brightness(img)
    img = brighter.enhance(2)

    # Crop image so that only the question and answers are visible
    img = img.crop((80, 280, 1000, 1400))

    return img

# Guess answer by getting info from google
def guessAnswer(myImage):

    # Start timer
    startTime = time.time()
    
    # Open image
    img = Image.open(myImage)
    
    # Convert image to text
    result = pytesseract.image_to_string(processImage(img))
    
    # Format question
    parts = result.split("\n\n")
    question = parts.pop(0).replace("\n", " ")
    parts = "\n".join(parts)
    parts = parts.split("\n")

    # In case pytesseract formats question/answers wrong
    if len(parts) > 3:
        # Format answers
        answers = [parts[-1], parts[-2], parts[-3]]
        
        for n in range(len(parts)-3):
            # Format question
            question = question + " "+parts[-len(parts)+n]
    else:
        # Format answers
        answers = list(parts)
    
    # Replace odd chars to increase guess accuracy
    for i, a in enumerate(answers):
        answers[i] = a.replace("ﬁ", "fi")
        answers[i] = a.replace("’", "'")
    question = question.replace("- ", "")
    question = question.replace("’", "'")

    # Searches the question on google 
    def searchGoogle(name):
        re = requests.get('https://www.google.com/search', params={'q':name})
        soup = BeautifulSoup(re.text, 'lxml')
        soup1 = str(soup)
        
        # Checks to see if an option exists in the google search
        if ((soup1.find(optA) != -1) or (soup1.find(optA.lower()) != -1)) or ((soup1.find(optB) != -1) or (soup1.find(optB.lower()) != -1)) or ((soup1.find(optC) != -1) or (soup1.find(optC.lower()) != -1)):
            return soup1

        # Gets a list of website links from google search, and searches first link
        else:
            # Find all <a> tags
            links = soup.findAll('a')
            linkList = []

            # Ignores unnecessary links and cleans up links
            for link in links:
                if (link['href'][:4] == '/url') and (link['href'].find('webcache.google') == -1):
                    link['href'] = link['href'].replace('/url?q=',"")
                    link['href'] = link['href'].replace(link['href'][link['href'].find('&sa=U&ved='):], "")
                    linkList.append(link['href'])

            # Get link of first website in google search
            re2 = requests.get(linkList[0])
            soup2 = BeautifulSoup(re2.text, 'lxml')
            soup2 = str(soup2)
            return soup2

    # Assign options to an index in answer list
    optA = answers[0]
    optB = answers[1]
    optC = answers[2]

    # Create a question answer list to display
    qa = [question, optA, optB, optC]
    print(qa)
    
    # Assign data to each option 
    testA = searchGoogle(question).find(optA)
    testB = searchGoogle(question).find(optB)
    testC = searchGoogle(question).find(optC)

    # Create a list of data and sort it
    ppl = [testA, testB, testC]
    ppl.sort()
    
    # Guess answer if it involves people in the answer
    if (question.find('Who') != -1) or (question.find('who') != -1):

        if ppl[1] == testA:
            print("answer is probably", optA)

        elif ppl[1] == testB:
            print("answer is probably", optB)

        else:
            print("answer is probably", optC) 

        print("--- %s seconds ---" % (time.time() - startTime))
        print("")
        startTime = 0

    # Guess answer if question asking something like "which is NOT ..."
    elif question.find('NOT') != -1:
        testALower = searchGoogle(question).find(optA.lower())
        testBLower = searchGoogle(question).find(optB.lower())
        if testALower == -1:
            print("answer is probably", optA)

        elif testBLower == -1:
            print("answer is probably", optB)

        else:
            print("answer is probably", optC) 

        print("--- %s seconds ---" % (time.time() - startTime))
        print("")
        startTime = 0   

    # Guess answer for general question     
    else:
        testALower = searchGoogle(question).find(optA.lower())

        if (testALower != -1) or (testA != -1):
            print("answer is probably", optA)

        elif (searchGoogle(question).find(optB.lower()) != -1) or (searchGoogle(question).find(optB) != -1):
            print("answer is probably", optB)

        else:
            print("answer is probably", optC)

        print("--- %s seconds ---" % (time.time() - startTime))
        print("")
        startTime = 0

# General usage
# guessAnswer('example.png')

guessAnswer('Q1.png')
