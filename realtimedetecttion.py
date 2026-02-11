from keras.models import model_from_json
import cv2
import numpy as np

json_file = open("signlanguagedetectionmodel48x48 (1).json", "r")
model_json = json_file.read()
json_file.close()

model = model_from_json(model_json)
model.load_weights("signlanguagedetectionmodel48x48 (2).h5")

print("Model loaded")

labels = ['Danger', 'Help', 'Peace', 'blank']  # must match training order


def extract_features(image):
    image = np.array(image)
    image = image.reshape(1, 48, 48, 1)
    image = image.astype("float32") / 255.0
    return image

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ROI box
    cv2.rectangle(frame, (50, 50), (300, 300), (0, 165, 255), 2)

    roi = frame[50:300, 50:300]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (48, 48))
    processed = extract_features(gray)

    # Prediction
    prediction = model.predict(processed, verbose=0)
    class_index = np.argmax(prediction)
    label = labels[class_index]
    confidence = np.max(prediction) * 100

    # Show result
    if label != 'blank' and confidence > 60:
        cv2.putText(frame,
                    f"{label} : {confidence:.2f}%",
                    (50, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2)

    cv2.imshow("Sign Language Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()


