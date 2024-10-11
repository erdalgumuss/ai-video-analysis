import logging
from flask import Flask
from routes.health import health_bp
from routes.video import video_bp
from utils.errorHandler import handle_404, handle_500
from config import config

# Flask uygulamasını başlat
app = Flask(__name__)

# Blueprintleri uygulamaya dahil et
app.register_blueprint(health_bp)
app.register_blueprint(video_bp)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB yükleme sınırı

# Ana sayfa rotası
@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to AI Video Analysis API</h1>", 200

# Hata yönetimi
app.register_error_handler(404, handle_404)
app.register_error_handler(500, handle_500)

# 'werkzeug' logger'ını al ve log seviyesini 'ERROR' olarak ayarla
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Flask uygulamasını çalıştır
if __name__ == '__main__':
    app.run(debug=config.DEBUG, port=config.PORT)
