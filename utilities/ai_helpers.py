import os
import cv2
import joblib
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

face_detector = cv2.CascadeClassifier(os.getenv('AI_FACE_MASK'))


def extract_face(img):
  try:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_points = face_detector.detectMultiScale(gray, 1.2, 5, minSize=(20, 20))
    return face_points
  except:
    return []


def identify_face(facearray):
  try:
      model = joblib.load(os.getenv('MODAL_PATH'))
      return model.predict(facearray)
  except Exception as error:
    return error


def add_face(id):
    try:
        face_img_paths = []
        user_image_folder = os.path.join(os.getenv("FACES_DIR"), id)
        if not os.path.isdir(user_image_folder): os.makedirs(user_image_folder)

        i, j = 0, 0
        cap = cv2.VideoCapture(0)
        while 1:
            _, frame = cap.read()
            faces = extract_face(frame)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 20), 2)
                cv2.putText(frame, f'Images Captured: {i}/{os.getenv("NIMGS")}', (30, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2, cv2.LINE_AA)
                if j % 5 == 0:
                    path = os.path.join(user_image_folder, f'{id}_{i}.jpg')
                    cv2.imwrite(path, frame[y:y + h, x:x + w])
                    face_img_paths.append(path)
                    i += 1
                j += 1
            if j == int(os.getenv("NIMGS")) * 5: break
            cv2.imshow('Adding new User', frame)
            if cv2.waitKey(1) == 27: break
        cap.release()
        cv2.destroyAllWindows()
        train_model()
        return face_img_paths
    except Exception as error:
        return error


def take_attendance():
    try:
        identified_participant_id = None
        cap = cv2.VideoCapture(0)
        _, frame = cap.read()
        if len(extract_face(frame)) > 0:
            (x, y, w, h) = extract_face(frame)[0]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (86, 32, 251), 1)
            cv2.rectangle(frame, (x, y), (x+w, y-40), (86, 32, 251), -1)
            face = cv2.resize(frame[y:y+h, x:x+w], (50, 50))
            identified_participant_id = identify_face(face.reshape(1, -1))[0]
            cv2.putText(frame, f'{identified_participant_id}', (x+5, y-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('Attendance', frame)
        cap.release()
        cv2.destroyAllWindows()
        return identified_participant_id
    except Exception as error:
        return error


def train_model():
    try:
        faces = []
        labels = []
        userlist = os.listdir(os.getenv("FACES_DIR"))
        for user in userlist:
            for imgname in os.listdir(os.path.join(os.getenv("FACES_DIR"), user)):
                img = cv2.imread(os.path.join(os.getenv("FACES_DIR"), user, imgname))
                resized_face = cv2.resize(img, (50, 50))
                faces.append(resized_face.ravel())
                labels.append(user)
        faces = np.array(faces)
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(faces, labels)
        joblib.dump(knn, os.getenv("MODAL_PATH"))
        return True
    except Exception as error:
        return error