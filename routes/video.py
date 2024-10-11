from flask import Blueprint
from controllers.videoController import process_video

video_bp = Blueprint('video', __name__)

# Video işleme rotası
@video_bp.route('/api/video/process', methods=['POST'])
def process():
    return process_video()
