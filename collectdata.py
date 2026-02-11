import cv2
import os

directory = 'SignImage48x48'
print(os.getcwd())

# Create main directory
if not os.path.exists(directory):
    os.mkdir(directory)

# Create required folders
required = ["Help", "Danger", "Peace", "blank"]
for f in required:
    path = os.path.join(directory, f)
    if not os.path.exists(path):
        os.mkdir(path)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Error: Camera not opened!")
    exit()

print("✅ Camera started. Press:")
print(" a = Help")
print(" b = Danger")
print(" c = Peace")
print(" . = blank")
print(" q = Quit")

while True:
    ret, frame = cap.read()

    if not ret:
        print("❌ Failed to grab frame")
        break

    count = {
        'a': len(os.listdir(os.path.join(directory, "Help"))),
        'b': len(os.listdir(os.path.join(directory, "Danger"))),
        'c': len(os.listdir(os.path.join(directory, "Peace"))),
        'blank': len(os.listdir(os.path.join(directory, "blank")))
    }

    cv2.rectangle(frame, (0, 40), (300, 300), (255, 255, 255), 2)
    cv2.imshow("data", frame)

    roi = frame[40:300, 0:300]
    cv2.imshow("ROI", roi)

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (48, 48))

    key = cv2.waitKey(10) & 0xFF

    if key == ord('a'):
        cv2.imwrite(os.path.join(directory, "Help", f"{count['a']}.jpg"), gray)
    if key == ord('b'):
        cv2.imwrite(os.path.join(directory, "Danger", f"{count['b']}.jpg"), gray)
    if key == ord('c'):
        cv2.imwrite(os.path.join(directory, "Peace", f"{count['c']}.jpg"), gray)
    if key == ord('.'):
        cv2.imwrite(os.path.join(directory, "blank", f"{count['blank']}.jpg"), gray)

    # Quit program
    if key == ord('q'):
        print("🛑 Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
