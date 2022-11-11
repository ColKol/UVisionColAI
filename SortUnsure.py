import yaml
import os
from tkinter import *
from PIL import Image, ImageTk
import imghdr

# open yaml files
yaml_file = open("UnsureItems.yml", 'r')
yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)

Unsure = yaml_content['Unsure']
training_photos = yaml_content['training_photos']
not_image = yaml_content['not_image']

#list of (non hidden) files in unsure folder
unsure_vehicles = [f for f in os.listdir(Unsure) if not f.startswith('.')]

#remove non-image files
for file in unsure_vehicles:
    FilePath = f'{Unsure}/{file}'
    if imghdr.what(FilePath) != 'jpeg'and imghdr.what(FilePath) != 'png':
        os.replace(f"{FilePath}", f"{not_image}/{file}")

#redefine file (unoptimal)
unsure_vehicles = [f for f in os.listdir(Unsure) if not f.startswith('.')]

def CreateWindow():
    ImageIndex = 0

    root = Tk()
    root.title("Sort Unsure")

    #create 1st image
    ImageSource = ImageTk.PhotoImage(Image.open(f'{Unsure}/{unsure_vehicles[ImageIndex]}'))
    ImageLabel = Label(image=ImageSource)
    ImageLabel.grid(row=0, column=0, columnspan=5)

    myLabel = Label(root, text=f"Sent to...")
    myLabel.grid(row=2, column=0, columnspan=5)

    #click function
    def MyClick(Classification):
        nonlocal myLabel
        nonlocal ImageLabel
        nonlocal ImageSource
        nonlocal ImageIndex

        ImageLabel.grid_forget()

        #send image to folder if button is not skip
        if Classification != 'skip':
            ImagePath = f'{Unsure}/{unsure_vehicles[ImageIndex]}'
            os.replace(f"{ImagePath}", f"{training_photos}/{Classification}/{unsure_vehicles[ImageIndex]}")

        myLabel.config(text=f'Sent to {Classification}')

        #Move to next image
        ImageIndex += 1

        #End window if all vehicles run through
        if ImageIndex >= len(unsure_vehicles):
            print('All vehicles sorted!')
            root.destroy()
            return

        #Show next image
        ImageSource = ImageTk.PhotoImage(Image.open(f'{Unsure}/{unsure_vehicles[ImageIndex]}'))
        ImageLabel = Label(image=ImageSource)
        ImageLabel.grid(row=0, column=0, columnspan=5) #original 5

    #Buttons class
    class SortButton:
        def __init__(self, ButtonColumn, ButtonText):
            self.ButtonColumn = ButtonColumn
            self.ButtonText = ButtonText
            ChooseButton = Button(root, text=ButtonText, padx=50, command=lambda: MyClick(ButtonText))
            ChooseButton.grid(row= 1, column=ButtonColumn)

    #for automation, can use learn.dls.vocab + 'skip' from fastai library
    ButtonsText = ['motorcycle', 'private_car', 'van', 'taxi', 'skip']
    for i in range (len(ButtonsText)):
        SortButton(i, ButtonsText[i])

    root.mainloop()

#only run if there are image files
if len(unsure_vehicles) > 0:
    CreateWindow()

else:
    print('No vehicles')
