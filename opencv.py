import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import messagebox
import psycopg2
import os
#from database import UpdateCoordinates


# Defining CreateWidgets() function to create necessary tkinter widgets
def createwidgets():

    destBrowse()

    root.feedlabel = Label(root, bg="black", fg="Tan", text="Webcamera", font=('Comic Sans MS', 20))
    root.feedlabel.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

    root.cameraLabel = Label(root, bg="white", borderwidth=10, relief="groove")
    root.cameraLabel.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

    root.saveLocationEntry = Entry(root, width=55, textvariable=destPath)
    root.saveLocationEntry.grid(row=5, column=1, padx=10, pady=10)

    root.captureBTN = Button(root, text="CAPTURE", command=Capture, bg="white",fg="Tan" ,font=('Times New Roman',
                                                                 15,"bold"), width=20,activebackground="green",cursor="hand2")

    root.captureBTN.grid(row=6, column=1, padx=10, pady=10)

    root.CAMBTN = Button(root, text="STOP CAMERA", command=StopCAM, bg="white",fg="Tan", font=('Comic Sans MS', 15),
                         width=13)
    root.CAMBTN.grid(row=4, column=2)

    root.previewlabel = Label(root, bg="white", fg="black", text="RESIZE IMAGE", font=('Comic Sans MS', 20))
    root.previewlabel.grid(row=1, column=4, padx=10, pady=10, columnspan=2)

    root.imageLabel = Label(root, bg="black", borderwidth=10, relief="groove")
    root.imageLabel.grid(row=2, column=4, padx=10, pady=10, columnspan=2)

    root.openImageEntry = Entry(root, width=55, textvariable=imagePath)
    root.openImageEntry.grid(row=5, column=4, padx=10, pady=10)

    root.logoutBtn = Button(root, text="Log out", width=20, bg="Tomato", font=('Comic Sans MS', 15), command="")
    root.logoutBtn.grid(row=15, column=2, padx=10, pady=10)

    ShowFeed()

'''
    frame1 = Frame(root, bg="black")
    frame1.place(x=1500, y=0, width=420, height=1060)

    #coordinates

    coordinates_label = Label(frame1, text="Coordinates", font=("goudy old", 20, "bold"), fg="Tan",
                                bg="black")
    coordinates_label.place(x=10, y=30)
    x_label = Label(frame1, text="X_coordinates : ", font=("goudy old", 10, "bold"), fg="Tan",
                        bg="black")
    x_label.place(x=50, y=80)
    global xcordinatesEntry
    xcordinatesEntry = Entry(frame1, width=8, textvariable=start_x)
    xcordinatesEntry.place(x=200, y=80)

    y_label = Label(frame1, text="Y_coordinates : ", font=("goudy old", 10, "bold"), fg="Tan",
                    bg="black")
    y_label.place(x=50, y=130)
    global ycordinatesEntry
    ycordinatesEntry = Entry(frame1, width=8, textvariable=start_y)
    ycordinatesEntry.place(x=200, y=130)

    width_label = Label(frame1, text="Width : ", font=("goudy old", 10, "bold"), fg="Tan",
                    bg="black")
    width_label.place(x=50, y=180)
    global widthEntry
    widthEntry = Entry(frame1, width=8, textvariable=end_x)
    widthEntry.place(x=200, y=180)

    height_label = Label(frame1, text="Height : ", font=("goudy old", 10, "bold"), fg="Tan",
                    bg="black")
    height_label.place(x=50, y=230)
    global heightEntry
    heightEntry = Entry(frame1, width=8, textvariable=end_y)
    heightEntry.place(x=200, y=230)

    root.UpdateBtn = Button(frame1, text="insert", width=15, bg="Tan", font=('Comic Sans MS', 15), command="")
    root.UpdateBtn.place(x=200, y=280)
    '''


    # Calling ShowFeed() function


# Defining ShowFeed() function to display webcam feed in the cameraLabel;
def ShowFeed():
    # Capturing frame by frame

    ret, frame = root.cap.read()

    if ret:

        # Displaying date and time on the feed
        cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20, 30), cv2.FONT_HERSHEY_DUPLEX, 0.5,
                    (0, 255, 255))


        # Changing the frame color from BGR to RGBA
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        # Creating an image memory from the above frame exporting array interface
        videoImg = Image.fromarray(cv2image)

        # Creating object of PhotoImage() class to display the frame
        imgtk = ImageTk.PhotoImage(image=videoImg)


        # Configuring the label to display the frame
        root.cameraLabel.configure(image=imgtk)

        # Keeping a reference
        root.cameraLabel.imgtk = imgtk

        # Calling the function after 10 milliseconds
        root.cameraLabel.after(10, ShowFeed)

    else:
        # Configuring the label to display the frame
        root.cameraLabel.configure(image='')


def destBrowse():

    path = os.getcwd()
    filename = "Image"
    file_path = os.path.join(path, filename)
    destPath.set(file_path)

def imageBrowse(fileName):
    # Presenting user with a pop-up for directory selection. initialdir argument is optional
    # Retrieving the user-input destination directory and storing it in destinationDirectory
    # Setting the initialdir argument is optional. SET IT TO YOUR DIRECTORY PATH
    #openDirectory = filedialog.askopenfilename(initialdir="")

    # Displaying the directory in the directory textbox
    imagePath.set(fileName)

    # Opening the saved image using the open() of Image class which takes the saved image as the argument
    imageView = Image.open(fileName)
    #imageCrop = imageView.crop(box=(int(start_x.get()),int(start_y.get()),int(end_x.get()),int(end_y.get())))

    # Creating object of PhotoImage() class to display the frame
    root.imageDisplay = ImageTk.PhotoImage(imageView)

    # Configuring the label to display the frame
    root.imageLabel.config(image=root.imageDisplay)

    # Keeping a reference
    root.imageLabel.photo = root.imageDisplay


    # Record starting (x,y) coordinates on left mouse button click



def onMouse(filename):
    root.imageDisplay = root.clone().copy()
    cv2.namedWindow('image')
    root.image_coordinates = []
    def extract_coordinates(event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            root.image_coordinates = [(x, y)]

        # Record ending (x,y) coordintes on left mouse button release
        elif event == cv2.EVENT_LBUTTONUP:
            root.image_coordinates.append((x, y))
            # print('top left: {}, bottom right: {}'.format(root.image_coordinates[0], root.image_coordinates[1]))
            # print('x,y,w,h : ({}, {}, {}, {})'.format(root.image_coordinates[0][0], root.image_coordinates[0][1],
            # root.image_coordinates[1][0] - root.image_coordinates[0][0],
            # root.image_coordinates[1][1] - root.image_coordinates[0][1]))

            # Draw rectangle
            cv2.rectangle(root.clone, root.image_coordinates[0], root.image_coordinates[1], (36, 255, 12), 2)


    cv2.setMouseCallback('image',extract_coordinates)


# Defining Capture() to capture and save the image and display the image in the imageLabel
def Capture():
    # Storing the date in the mentioned format in the image_name variable
    image_name = datetime.now().strftime('%d-%m-%Y %H-%M-%S')
    '''
    # If the user has selected the destination directory, then get the directory and save it in image_path
    if destPath.get() != '':
        image_path = destPath.get()
    # If tuser has not selected any destination directory, then set the image_path to default directory
    else:
        messagebox.showerror("ERROR", "NO DIRECTORY SELECTED TO STORE IMAGE!!")
    '''
    image_path = destPath.get()
    # Concatenating the image_path with image_name and with .jpg extension and saving it in imgName variable
    imgName = image_path + '/' + image_name + ".jpg"

    # Capturing the frame
    ret, frame = root.cap.read()

    # Displaying date and time on the frame
    cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20, 30), cv2.FONT_HERSHEY_DUPLEX, 0.5,
                (0, 255, 255))

    # Writing the image with the captured frame. Function returns a Boolean Value which is stored in success variable
    success = cv2.imwrite(imgName, frame)



    # Opening the saved image using the open() of Image class which takes the saved image as the argument
    saved_image = Image.open(imgName)

    # Creating object of PhotoImage() class to display the frame
    saved_image = ImageTk.PhotoImage(saved_image)

    imageBrowse(imgName)





# Defining StopCAM() to stop WEBCAM Preview
def StopCAM():
    # Stopping the camera using release() method of cv2.VideoCapture()
    root.cap.release()

    # Configuring the CAMBTN to display accordingly
    root.CAMBTN.config(text="START CAMERA", command=StartCAM)

    # Displaying text message in the camera label
    root.cameraLabel.config(text="OFF CAM", font=('Comic Sans MS', 70))

def StartCAM():
    # Creating object of class VideoCapture with webcam index
    root.cap = cv2.VideoCapture(0)

    # Setting width and height
    width_1, height_1 = 600, 650
    root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_1)
    root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height_1)

    # Configuring the CAMBTN to display accordingly
    root.CAMBTN.config(text="STOP CAMERA", command=StopCAM)

    # Removing text message from the camera label
    root.cameraLabel.config(text="")

    # Calling the ShowFeed() Function


    ShowFeed()


# Creating object of tk class
root = tk.Tk()

# Creating object of class VideoCapture with webcam index
root.cap = cv2.VideoCapture(0)

# Setting width and height
width, height = 600, 650
root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Setting the title, window size, background color and disabling the resizing property
root.title("pycam")
root.geometry("1920x1060")
root.resizable(False, False)
root.configure(background="White")

# Creating tkinter variables
destPath = StringVar()
imagePath = StringVar()

start_x = StringVar()
start_y = StringVar()
end_x = StringVar()
end_y = StringVar()



createwidgets()
root.mainloop()

