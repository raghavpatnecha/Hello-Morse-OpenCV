from flask import Flask, render_template, Response
from morse_camera import Camera
from morse_eyes import Detectmorse
import time
from morse_log import log

app = Flask(__name__)
morse = Detectmorse()

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        png, L = morse.calculate(frame)
        streambyte()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + png.tobytes() + b'\r\n')




@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/yield')
def streambyte():
    L = morse.L
    final = morse.final
    #print("raghav",L)

    b = (''.join(L)).encode('utf-8')
    c = (final).encode('utf-8')
    log(b)
    log(c)
    def events():
        yield "data: %s %s\n\n" % (b,c)
        time.sleep(1)  # an artificial delay
    return Response(events(), content_type='text/event-stream')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
