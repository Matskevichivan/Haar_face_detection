# Usage example: python3 haar_face_detection.py --folder=data/originalPics/2002/07/19/big/ --xml=haarcascade_frontalface_default.xml

# import the necessary packages
import cv2 as cv
import argparse
import os
import json
import time


# Construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--folder", required = True, 
	help = "path to folder with images")
ap.add_argument("-x", "--xml", required = True, 
    help = "path to haarcascade xml file")
args = ap.parse_args()

print("[INFO] loading model...")
# Load the required XML classifiers
face_cascade = cv.CascadeClassifier(args.xml)

# Path to test image
path  = 'test_images/img_140.jpg'

# List of dictionary
annotation = []

# Make dirictory if it isn't here
if not os.path.isdir('images/'):
    os.makedirs('images/')

def load_images_from_folder(path):
    """Load images from the folder

    Keyword arguments:
    path -- path to folder with images

    """

    for (i,filename) in enumerate(os.listdir(path)):
        if filename.split('.')[-1].lower() in {'jpeg', 'jpg', 'png'}:
            load_images_to_folder(path + filename, i)

def face_detection(image):
    """Detect faces on image

    Keyword argument:
    image -- path to input image
    key   -- number of detected image

    """

    # Load input image
    # img = cv.imread(image)
    # Convert to grayscale mode
    #print(image)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
 
    return faces

def load_images_to_folder(image, key):
    """Make json file with result"""

    # List of coordinats
    coor = []
    # Start number of faces
    k = 1

    # Load input image
    img = cv.imread(image)

    # Number of faces
    faces = face_detection(img)
    #print(len(faces))
   
    # Check if the persons who have been detected
    # if no faces assign a value 0 
    if len(faces) == 0:
        faces = 0
        print("Number of faces detected: " + str(faces))

        # Resize image in a half
        cv.resize(img,(0,0), fx = 0.5, fy = 0.5)
        # Write image in a folder images
        cv.imwrite(os.path.join('images/', "image-" + str(key) + ".jpg"), img)

        # Create dictionary with coordinats = None
        json_dict = create_dict(None, faces, key)
        # Add dictionary in the list
        annotation.append(json_dict)
        with open('result.json', 'w') as f:
            # Write the results
            f.write(json.dumps(annotation))
    # else find all faces coordinats
    else:
        print("Number of faces detected: " + str(faces.shape[0]))
        for (x,y,w,h) in faces:
                #cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

                # Create a filter
                blurred = cv.GaussianBlur(img,(25,25),0)
                # Change the detected faces to blurring
                img[y:y+h,x:x+w] = blurred[y:y+h,x:x+w]

                coor.append([x,y,x+w,y+h])

                # Draw number of faces detection on image
                #cv.putText(img, "Number of faces detected: " + str(faces.shape[0]), (0,img.shape[0] -10), cv.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,0), 1)
                #cv.rectangle(img, ((0,img.shape[0] -25)),(270, img.shape[0]), (255,255,255), -1)
                
                # resize image in a half
                cv.resize(img, (0,0), fx = 0.5, fy = 0.5)
                # Only if detected all faces in the image
                if  k == faces.shape[0]:

                    # Write image in a folder images
                    cv.imwrite(os.path.join('images/', "image-" + str(key) + ".jpg"), img)

                    json_dict = create_dict(str(coor), faces.shape[0], key)
                    # Add dictionary in the list
                    annotation.append(json_dict)

                    with open('result.json', 'w') as f:
                        # Write the results
                        f.write(json.dumps(annotation))
                # If not all the faces in the image are detecting,add number of faces
                else:
                    k+=1
                         

def create_dict(bbox, faces, key):
    """Return the dictionary

    Keyword argument:
    bbox  -- list of the faces coordinats
    faces -- number of faces detected
    key   -- number of detected image

    """

    d = { "Image": 'image-' + str(key) + 'jpg',
          "Number of faces detected: " : str(faces),
          "Coordinats:" : bbox}
    return d


if __name__ == "__main__":

    # Start time counter
    start_time = time.time()

    load_images_from_folder(args.folder)

    # Test the function
    if len(face_detection(cv.imread(path))) == 1:
        print('Test is OK')
    else:
        print('Test is Fail')

    # Print time spent on image processing
    print('[INFO] elapsed time: {:.2f}s'.format(time.time()-start_time))
    print('[INFO] all images are detecting')

