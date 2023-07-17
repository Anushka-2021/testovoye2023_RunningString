import os.path
import sqlite3, numpy as np, requests, cv2
from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)

conn = sqlite3.connect("usingdb.db", check_same_thread=False)
cursor = conn.cursor()

@app.route('/', methods = ['POST', 'GET'])
def sending():
    if request.method == 'POST':
        if request.form.get('path') is None:
            path = 'C:/running_strings'
        else:
            path = request.form.get('path')
        if not os.path.exists(path) or not os.path.isdir(path):
                os.makedirs(path)

        if request.form.get('name') is not None and request.form.get('name') != "":
            name = request.form.get('name')
        else:
            name = 'running_text'

        text = request.form.get('entr')

        image = np.zeros((100, 100, 3), dtype=np.uint8)
        # Text parameters
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_color = (255, 255, 255)  # White
        line_type = cv2.LINE_AA

        # Video parameters
        fps = 30
        video_length = 3
        total_frames = fps * video_length

        # Video creation
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(path + '/' + name + '.mp4', fourcc, fps, (100, 100))

        text_width, text_height = cv2.getTextSize(text, font, font_scale, 1)[0]
        x = 100
        y = 50
        for frame_number in range(total_frames):
            image.fill(0)

            # Drawing text into video and pushing it into existing video
            cv2.putText(image, text, (x, y), font, font_scale, font_color, 1, line_type)
            video_writer.write(image)

            x-=(text_width+200)//total_frames # offset
        video_writer.release()

        # Adding into database
        f = list(cursor.execute("SELECT count(*) FROM myStrings1"))[0][0]
        cursor.execute("INSERT OR REPLACE INTO myStrings1(string_id, string_body, time_of_sending) VALUES (?, ?, ?)", (f+1, text, datetime.now()))
    return render_template("test.html")

@app.route('/down_page', methods = ['POST', 'GET'])
def down_page():
    if request.method == 'POST':
        text = request.form.get('entr')

        image = np.zeros((100, 100, 3), dtype=np.uint8)
        # Text parameters
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_color = (255, 255, 255)  # White
        line_type = cv2.LINE_AA

        # Video parameters
        fps = 30
        video_length = 3
        total_frames = fps * video_length
        # Video creation
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter('static/running_text.mp4', fourcc, fps, (100, 100))
        text_width, text_height = cv2.getTextSize(text, font, font_scale, 1)[0]
        x = 100
        y = 50
        for frame_number in range(total_frames):
            image.fill(0)

            # Drawing text into video and pushing it into existing video
            cv2.putText(image, text, (x, y), font, font_scale, font_color, 1, line_type)
            video_writer.write(image)

            x-=(text_width+200)//total_frames # offset
        video_writer.release()

        # Adding into database
     #   f = list(cursor.execute("SELECT count(*) FROM myStrings1"))[0][0]
      #  cursor.execute("INSERT OR REPLACE INTO myStrings1(string_id, string_body, time_of_sending) VALUES (?, ?, ?)", (f+1, text, datetime.now()))
        return render_template("download.html")
    return render_template("index.html")

if __name__ == '__main__':
    cursor.execute("""CREATE TABLE IF NOT EXISTS myStrings1
    (string_id UNIQUE, string_body, time_of_sending)
    """)
    conn.commit()

    app.run(debug=True)