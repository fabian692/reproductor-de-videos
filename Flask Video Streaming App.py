from flask import Flask, render_template, request, redirect, url_for
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# Directorio para almacenar videos
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'mp4', 'webm', 'ogg'}

# Crear directorio si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Simulación de base de datos en memoria
videos = []

@app.route('/')
def index():
    return render_template('index.html', videos=videos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        title = request.form.get('title')
        description = request.form.get('description')
        
        if file and allowed_file(file.filename):
            filename = f"{uuid.uuid4()}.{file.filename.rsplit('.', 1)[1].lower()}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Agregar video a la lista
            videos.append({
                'id': len(videos) + 1,
                'title': title or 'Sin título',
                'description': description or 'Sin descripción',
                'filename': filename,
                'upload_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/video/<int:video_id>')
def video(video_id):
    video = next((v for v in videos if v['id'] == video_id), None)
    if video:
        return render_template('video.html', video=video)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)