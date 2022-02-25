from flask import Flask, render_template,request,flash,Response
import cv2
from pyzbar.pyzbar import decode
import numpy as np

app = Flask(__name__, template_folder='./templates')
flag=None

def read_QR (img):
    global flag
    for barcode in decode(img):
        my_data = barcode.data.decode('utf-8')
        print(my_data)
        flag=my_data
        pts = np.array([barcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        img1 = cv2.polylines(img,[pts],True,(255,0,255),5)
        pts2 = barcode.rect
        img= cv2.putText(img1,my_data, (pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,255),2)
        return img


cap = cv2.VideoCapture(1)
def gen_frames():  # generate frame by frame from camera
    while True:
        success, img = cap.read()
        read_QR(img)
        try:
            ret, buffer = cv2.imencode('.jpg', cv2.flip(img, 1))
            img = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
        except Exception as e:
            pass
        else:
            pass

@app.route('/')
def result():
    return render_template('w.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/',methods= ['POST'])
def cal ():
    global flag
    return render_template('w.html', flag =  flag )

if __name__ == '__main__':
    app.run(debug=True)