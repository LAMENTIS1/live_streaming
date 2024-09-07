from flask import Flask, Response
import cv2

app = Flask(__name__)

def generate_frames():
    # Open the first camera device (0 for the default camera)
    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode the frame in JPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Yield the frame in the format required for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/live_feed')
def live_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '''
        <html>
        <body>
            <h1>Camera Feed</h1>
            <img src="/live_feed" width="640" height="480" />
            <br>
            <button onclick="startStreaming()">Start Streaming</button>
            <script>
                function startStreaming() {
                    const img = document.querySelector('img');
                    img.src = "/live_feed";
                }
            </script>
        </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Host on all available IP addresses
