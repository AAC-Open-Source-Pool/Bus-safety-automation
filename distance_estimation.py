import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
cap = cv2.VideoCapture(0)
dectector=FaceMeshDetector(maxFaces=1)



while True:
    K,img=cap.read()
    img,faces=dectector.findFaceMesh(img,draw=False)
    if faces:
        face=faces[0]
        try:
            (x, y),( w, h) = face[103],face[400] # Top-left corner (x, y) and width (w), height (h)

            # Draw bounding box
           # cv2.rectangle(img, (x, y), (  w, h), (255, 0, 255), 2)  # Blue box with thickness 2
        except: 
            pass
        pointLeft=face[145] #point pointing to center of left eye 
        pointright=face[374] #point pointing to center of right eye ,to find distance between the eyes
        #cv2.circle(img,pointLeft,5,(255,0,0),cv2.FILLED)
        #cv2.circle(img,pointright,5,(255,0,0),cv2.FILLED)    
        #cv2.line(img,pointLeft,pointright,(0,255,0),3)
        w,_= dectector.findDistance(pointLeft,pointright)
        #FINDING FOCAL LENGTH
        W=6.3
        #d=30
        #f=(w*d)/W
        #print(f)  
        #finding distance
        f=502
        d=(W*f)/w 
        print(d)    
        cvzone.putTextRect(img,f'Depth: {int(d)}cm',(face[10][0]-100,face[10][1]-50),scale=2)
    cv2.imshow("Image",img)
    if cv2.waitKey(1)==ord('q'):
        break
cap.release()

cv2.destroyAllWindows()

cap = cv2.VideoCapture(0)
dectector = FaceMeshDetector(maxFaces=1)
faceCascade = cv2.CascadeClassifier("project/face.xml")


def generate_dataset(img, id, img_id):
    cv2.imwrite("project/data/users." + str(id) + "." + str(img_id) + ".jpg", img)


# function to draw boundary around the face
def boundary_of_face(img, classifier, scalefactor, minNeighbors, color, text, clf):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray_img, scalefactor, minNeighbors)
    coordinates = []
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        k, _ = clf.predict(gray_img[y:y + h, x:x + w])
        if k == 1:
            cv2.putText(img, text, (x, y - 4), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coordinates = [x, y, w, h]
    return coordinates, img


def recon(img, clf, faceCascade):
    color = {"blue": (255, 0, 0), "red": (0, 0, 255), "green": (0, 225, 0)}
    coordinates, img = boundary_of_face(img, faceCascade, 1.1, 40, color['blue'], "VISHAL", clf)
    return img


# function to detect face using harcascade xml file and returning image

def detect(img, faceCascade):
    color = {"blue": (255, 0, 0), "red": (0, 0, 255), "green": (0, 225, 0)}
    coordinates, img = boundary_of_face(img, faceCascade, 1.1, 10, color['green'], "name..", clf)
    if len(coordinates) == 4:
        required_img = img[coordinates[1]:coordinates[1] + coordinates[3],
                       coordinates[0]:coordinates[0] + coordinates[2]]

        generate_dataset(required_img, user_id, img_id)
    return img


img_id = 0
user_id = 0
clf = cv2.face.LBPHFaceRecognizer_create()
clf.read("classifier.yml")

while True:
    ret, img = cap.read()
    # img=detect(img,faceCascade)
    img = recon(img, clf, faceCascade)

    img, faces = dectector.findFaceMesh(img, draw=True)
    if faces:
        face = faces[0]
        pointLeft = face[145]  # point pointing to center of left eye
        pointright = face[374]  # point pointing to center of right eye ,to find distance between the eyes
        cv2.circle(img, pointLeft, 5, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, pointright, 5, (255, 0, 0), cv2.FILLED)
        cv2.line(img, pointLeft, pointright, (0, 255, 0), 3)
        w, _ = dectector.findDistance(pointLeft, pointright)
        # FINDING FOCAL LENGTH
        W = 6.3
        # d=50
        # f=(w*d)/W
        # print(f)
        # finding distance
        f = 699
        d = (W * f) / w
        print(d)
        cvzone.putTextRect(img, f'Depth: {int(d)}cm', (face[10][0] - 100, face[10][1] - 50), scale=2)
    cv2.imshow("Image", img)

    if cv2.waitKey(1) == ord('q'):
        break
cap.release()

cv2.destroyAllWindows()