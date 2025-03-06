from turtle import delay

from flask import Flask, render_template, Response, request
import threading
import cv2
import winsound

app = Flask(__name__)

selected_frequency = 4000
selected_security = 1
selected_sensibility = 30

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_frequency', methods=['POST'])
def set_frequency():
    global selected_frequency
    selected_frequency = int(request.form['frequency'])
    print(f"Selected frequency: {selected_frequency} Hz")
    return render_template('index.html')

@app.route('/set_security', methods=['POST'])
def set_security():
    global selected_security
    selected_security = int(request.form['security'])
    print(f"Status security: {selected_security}")
    return render_template('index.html')

@app.route('/set_sensibility', methods=['POST'])
def set_sensibility():
    global selected_sensibility
    selected_sensibility = int(request.form['sensibility'])
    print(f"Selected sensibility: {selected_sensibility}")
    return render_template('index.html')


@app.route('/liveFeed')
def live_feed():
    return Response(video_player(), mimetype='multipart/x-mixed-replace; boundary=frame')

def alarm():
    global movement
    movement = False
    if not movement:
        winsound.Beep(selected_frequency, 1000)
        #delay(1000)
        print(f"Movement detected, beep at {selected_frequency} Hz")
    movement = True

camera = cv2.VideoCapture(0)
movement = True
movement_detected = 0

def video_player():
    global movement_detected, movement
    ret, frame1 = camera.read()
    ret, frame2 = camera.read()

    while True:
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (19, 19), 0)
        _, thresh = cv2.threshold(blur, 30, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if selected_security == 1:
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                if cv2.contourArea(contour) < 800: #900
                    continue
                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame1, "Movement", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            if thresh.sum() > 300:
                movement_detected += 1
            else:
                if movement_detected > 0:
                    movement_detected -= 1

            if movement_detected > selected_sensibility:
                if movement:
                    threading.Thread(target=alarm).start()
                if movement_detected > 0:
                    movement_detected -= 1

        ret, jpeg = cv2.imencode('.jpg', frame1)
        frame1 = frame2
        ret, frame2 = camera.read()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

if __name__ == '__main__':
    app.run(debug=True)
