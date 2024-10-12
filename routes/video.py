from flask import Blueprint
from controllers.videoController import process_video, analyze_video_gestures, evaluate_interview_results


video_bp = Blueprint('video', __name__)

# Video işleme rotası
@video_bp.route('/api/video/process', methods=['POST'])
def process():
    return process_video()

# Jest ve mimik analizi rotası
@video_bp.route('/api/video/analyze_gestures', methods=['POST'])
def analyze_gestures_route():
    return analyze_video_gestures()

@video_bp.route('/api/video/evaluate', methods=['POST'])
def evaluate_video():
    return evaluate_interview_results()
