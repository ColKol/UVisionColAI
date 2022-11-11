#Should be accompanied by yaml file with folder & .pkl (AI) directories

#YAML
import yaml
from yaml.loader import SafeLoader

#FastAI
from fastai.vision.all import *

#Folder management
import os
import time
import imghdr
import threading

# open yaml file
yaml_file = open("UVisionConfig.yml", 'r')
yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)

#Getting directories from YAML
vehicles_new = yaml_content['WatchFolder'] #useless as new system uses in and out gates
vehicles_done = yaml_content['DoneFolder'] #not useless do not delete

#Multiple folder checks
InGate = yaml_content['InGate']
OutGate = yaml_content['OutGate']

#bin for files that are not images
not_image = yaml_content['not_image']

#Load model
Model = yaml_content['Model']
learn = load_learner(Model)

ConfidenceThreshold = yaml_content['ConfidenceThreshold']

#function that sorts images
def SortImage(TargetPhoto, TimeID, Folder):
    print(f'target: {TargetPhoto}')
    ImagePath = f"{Folder}/{TargetPhoto}"
    print(f'Image path: {ImagePath}')

    #Check file is valid image
    if imghdr.what(ImagePath) != 'jpeg' and imghdr.what(ImagePath) != 'png':
        os.replace(f"{ImagePath}", f"{not_image}/{TargetPhoto}")
        return

    #Predict image and get probability
    Prediction, Pred_ID, Probs = learn.predict(ImagePath)
    Confidence = Probs[Pred_ID]

    #print(f'Image Name: {TargetPhoto}')
    #print(f'Image Path: {ImagePath}')
    #print(f'Prediction: {Prediction}')
    #print(f'Confidence: {Confidence}')

    if Confidence > ConfidenceThreshold:
        os.replace(f"{ImagePath}", f"{vehicles_done}/{Prediction}/{Prediction}_{TimeID}_{Confidence:.2f}.jpg")
        print(f'sent to {Prediction}')
    else:
        os.replace(f"{ImagePath}", f"{vehicles_done}/unsure/{Prediction}_{TimeID}_{Confidence:.2f}.jpg")
        print('sent to unsure')
    # Remember the .jpg!

print('Running:')

def Monitor(Folder):
    while(True):
        print(Folder)

        #creates list of items and removes files starting with . (hidden)
        vehicles_new_images = [f for f in os.listdir(Folder) if not f.startswith('.')]
        print(f'List: {vehicles_new_images}')

        #Check for images in vehicles_new folder
        if len(vehicles_new_images) > 0:
            i = 0
            time_object = time.localtime()
            OldTime = time.strftime("%y-%m-%d-%H-%M-%S", time_object)
            
            for vehicle in vehicles_new_images:
                #get current time to avoid duplicates
                time_object = time.localtime()
                NewTime = time.strftime("%y-%m-%d-%H-%M-%S", time_object)
                
                #if files were sorted in the same second, order them
                if NewTime == OldTime:
                    i += 1
                    OldTime = NewTime
                else:
                    i = 0
                    OldTime = NewTime
                TimeID = NewTime + '-' + str(i)
                SortImage(vehicle, TimeID, Folder)
        time.sleep(1)

t1 = threading.Thread(target=Monitor, args=(InGate,))
t2 = threading.Thread(target=Monitor, args=(OutGate,))

#starting therads
t1.start()
t2.start()

# wait until threads are completely executed
t1.join()
t2.join()

#Exceptions
    # check if is jpg or png done
    # 2 cameras (in & out) (monitor 2 folders & in gate done out gate done)
