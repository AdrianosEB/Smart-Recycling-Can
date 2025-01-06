from keras.models import load_model
import cv2
import numpy as np
import serial
import time

# Port Communicaiton
try:
    ser = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2) 
    serial_connected = True
    print("Portal com successful")
except serial.SerialException:
    ser = None
    serial_connected = False
    print("No portal com")


camera = cv2.VideoCapture(2)
camera.set(3, 640)
camera.set(4, 480)

if not camera.isOpened():
    print("no cam")
    exit()


# Load model
model = load_model("custom_model.h5")
class_names = ["EmptyPlate", "NonRecycled", "Recycled"]

try:
    while True:
        print("waiting")
        time.sleep(2)


        ret, image = camera.read()
        if not ret:
            print("no img from cam")
            break

        resized_image = cv2.resize(image, (224, 224))
        model_input = np.expand_dims(resized_image / 127.5 - 1, axis=0)

        # predict class
        prediction = model.predict(model_input)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        # send to serial
        if serial_connected:
            ser.write(str(index).encode())
            print(f"Sent to port: {index}")
        else:
            print(f"Not sent to port: Predicted Class {index} ({class_name}), Confidence Score: {confidence_score:.2f}")

        # show result on window
        display_text = f"{class_name}: {confidence_score:.2f}"
        cv2.rectangle(image, (10, 10), (400, 50), (255, 0, 0), -1)
        cv2.putText(image, display_text, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Real-Time Classification", image)

        if cv2.waitKey(1) & 0xFF == 27:
            print("Ending")
            break

finally:
    camera.release()
    if serial_connected:
        ser.close()
    cv2.destroyAllWindows()
