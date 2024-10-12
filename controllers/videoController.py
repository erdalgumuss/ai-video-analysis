import os
from flask import request, jsonify
from services.transcription_service import process_video_transcription
from services.gesture_analysis_service import analyze_gestures
from services.evaluation_service import evaluate_interview


# Yardımcı Fonksiyonlar
def ensure_uploads_directory_exists():
    """'uploads' klasörünün var olup olmadığını kontrol et ve yoksa oluştur."""
    if not os.path.exists('./uploads'):
        os.makedirs('./uploads')


def save_video(video_file):
    """Video dosyasını kaydeder."""
    video_path = f"./uploads/{video_file.filename}"
    ensure_uploads_directory_exists()
    video_file.save(video_path)
    print(f"Video dosyası kaydedildi: {video_path}")
    return video_path


def remove_video(video_path):
    """Kaydedilen video dosyasını siler."""
    if os.path.exists(video_path):
        os.remove(video_path)
        print(f"Video dosyası silindi: {video_path}")


def handle_video_upload():
    """Video dosyasını request'ten alır ve kaydeder."""
    if 'video' not in request.files:
        return None, jsonify({"error": "No video file provided"}), 400

    video_file = request.files['video']
    video_path = save_video(video_file)
    return video_path, None, None


# Asıl İşlevler
def process_video():
    """Transkript çıkarma işlemi"""
    video_path, error, status_code = handle_video_upload()
    if error:
        return error, status_code

    # Transkript çıkar
    transcription = process_video_transcription(video_path)
    print(f"Çıkarılan transkript: {transcription}")

    # Video dosyasını sil
    remove_video(video_path)

    # Sonucu döndür
    return jsonify({"transcription": transcription}), 200


def analyze_video_gestures():
    """Jest ve mimik analizi yapma işlemi"""
    print("analyze_video_gestures() fonksiyonu çağrıldı.")

    video_path, error, status_code = handle_video_upload()
    if error:
        return error, status_code

    # Jest ve mimik analizini yap
    print("Jest ve mimik analizi başlatılıyor...")
    gesture_data = analyze_gestures(video_path)

    # Eğer gesture_data boşsa, bir hata döndürelim
    if not gesture_data:
        print("Hiçbir jest verisi tespit edilmedi.")
        remove_video(video_path)
        return jsonify({"error": "No gesture data detected"}), 400

    # Video dosyasını sil
    remove_video(video_path)

    # Sonucu döndür
    return jsonify({"gesture_analysis": gesture_data}), 200


def evaluate_interview_results():
    """Mülakat sonuçlarını değerlendirme işlemi"""
    video_path, error, status_code = handle_video_upload()
    if error:
        return error, status_code

    # Transkript çıkar
    transcription = process_video_transcription(video_path)

    # Jest ve mimik analizini yap
    gesture_data = analyze_gestures(video_path)

    # Tüm verileri değerlendir
    evaluation_result = evaluate_interview(transcription, gesture_data)

    # Video dosyasını sil
    remove_video(video_path)

    # Sonucu döndür
    print(evaluation_result)
    return jsonify(evaluation_result), 200
