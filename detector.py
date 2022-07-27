# Facial Detection using OpenCV and PySimpleGUI
# By gingernikki

import PySimpleGUI as UI
import cv2
import os

## LOCAL CONFIG
# This config is not saved (yet) and will need to be configured each time the program is opened
class cfg:
    r, g, b = 255, 255, 255
    shape = 'circle';

## GUIs

def selectfilewindow():
    UI.theme('SystemDefault');
    # Default filename text
    filename = 'Select a file to analyze...'
    # Background color of the window
    UI.SetOptions(background_color = '#dbdbdb');
    layout = [
        [UI.FileBrowse('Browse', key='filepath', file_types=(('Image Files', '*.jpg'), ('Image Files', '*.png')), button_color=('black', 'white'), size=8, pad=((0,4),(0,0))), UI.Text(" "*14),UI.Button('Settings', key='settings', button_color=('black', 'white'),size=8, pad=((0,4),(0,0)))],
        [UI.Text(filename, size=20, font=('Helvetica', 8), justification='center')],
        [UI.Button('Recognize', key='recognize', button_color=('black', 'white'), size=25)]
    ]
    # Listen for events
    event, values = UI.Window(title='Facial Detection', layout=layout, finalize=True).read()
    while True:

        # On the "Recognize" button click
        if event == 'recognize':
            # Return the filepath
            return values['filepath']
        if event == 'settings':
            # Open the settings window
            settingswindow();
            continue
        break

def settingswindow():
    settingslayout = [
        [UI.Text('Settings Panel', size=20, font=('Helvetica', 8), justification='center')],
        [UI.Button('Save', key='save', button_color=('black', 'white'), size=25)],
        [UI.Button('Cancel', key='cancel', button_color=('black', 'white'), size=25)]
    ]
    eventListener, value = UI.Window(title='Settings', layout=settingslayout, finalize=True).read()
    while True:
        if eventListener == 'save':
            # Get the drawtype
            drawtype = value['drawtype']
        elif eventListener == 'cancel':
            # Close the settings window
            UI.Window.Close(eventListener)
        break

## OPENCV STUFF

# Detect faces using cv2 and draw a rectangle around them
def detectfaces(filepath, drawtype):
    img = cv2.imread(filepath)
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Load the face detector dataset
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # Draw circle around the faces
    if drawtype == "circle":
        for (x,y,w,h) in faces:
            cv2.circle(img, (x+w//2, y+h//2), w//2, (255,255,255), 3)
    elif drawtype == "rectangle":
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255), 3)
    # Return the image
    if len(faces) == 0:
        print("Error: No faces detected in the image", filepath)
    else:
        return img

# Display an image with PySimpleGUI

def showimage(img):
    # Show the image
    cv2.imshow('img', img)
    # Wait for a key press
    cv2.waitKey(0)
    # Destroy the window
    cv2.destroyAllWindows()


## MODES

def manual(drawtype):
    # Get file manually
    imgPath = selectfilewindow();
    # Detect faces
    finalImage = detectfaces(imgPath, drawtype);
    # Show the image
    showimage(finalImage);
    # Save the image to a file in the output folder
    # Default output file name and type
    fileName = "manual_output"
    # Get the file type of imgPath
    fileType = imgPath.split('.')[-1]
    # Save the image
    cv2.imwrite('data/output/'+fileName + '.' + fileType, finalImage)
def auto(drawtype):
    # for each file in the input folder (data/input)
        for file in os.listdir('data/input'):
            cPath = 'data/input/' + file
            # Detect faces
            finalImage = detectfaces(cPath, drawtype);
            # Save the image to a file in the output folder
            # Default output file name and type
            fileName = cPath.split('.')[0].split('/')[-1]+"_output"
            fileType = cPath.split('.')[-1]
            # Get the file type of imgPath
            # Save the image
            cv2.imwrite('data/output/'+fileName + '.' + fileType, finalImage)