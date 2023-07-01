# This is a sample Python script.
import sqlite3, numpy as np, requests, cv2
from flask import Flask, request, render_template

app = Flask(__name__)

conn = sqlite3.connect("usingdb.db")
cursor = conn.cursor()

@app.route('/', methods = ['POST', 'GET'])
def sending():
    if request.method == 'POST':
        str = request.form.get('entr')
        print(str)
    return render_template("test.html")

if __name__ == '__main__':
    cursor.execute("""CREATE TABLE IF NOT EXISTS myStrings1
    (string_id UNIQUE, string_body, time_of_sending)
    """)
    conn.commit()

    image = np.zeros((100, 100, 3), dtype=np.uint8)
    # Устанавливаем параметры текста
    text = "Hello, World!"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (255, 255, 255)  # Белый цвет текста
    line_type = cv2.LINE_AA

    # Определяем параметры видео
    fps = 30  # Количество кадров в секунду
    video_length = 3  # Длина видео в секундах
    total_frames = fps * video_length

    # Создаем объект записи видео
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter('running_text.mp4', fourcc, fps, (100, 100))
    print(total_frames)
    # Генерируем видео
    text_width, text_height = cv2.getTextSize(text, font, font_scale, 1)[0]
    x = 0#(100 - text_width) // 2
    y = (100 + text_height) // 2
    for frame_number in range(total_frames):
        # Очищаем изображение
        image.fill(0)

        # Вычисляем позицию бегущей строки на текущем кадре
       # print(text_width, 100 - text_width, (100-text_width) // 2)

        print(x, y)
       # print(frame_number, text_width, text_width/total_frames)

        # Рисуем текст на изображении
        cv2.putText(image, text, (x, y), font, font_scale, font_color, 1, line_type)

        # Записываем кадр в видео
        video_writer.write(image)

        x-=text_width//total_frames
    # Закрываем объект записи видео
    video_writer.release()
    app.run(debug=True)
    print("!")
