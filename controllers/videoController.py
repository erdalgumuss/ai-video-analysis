import os
from flask import request, jsonify
from services.transcription_service import process_video_transcription

def process_video():
    # Kullanıcının yüklediği video dosyasını al
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400
    
    video_file = request.files['video']
    video_path = f"./uploads/{video_file.filename}"
    
    # 'uploads' klasörünün var olup olmadığını kontrol et ve yoksa oluştur
    if not os.path.exists('./uploads'):
        os.makedirs('./uploads')
    
    # Video dosyasını sunucuda geçici olarak kaydet
    video_file.save(video_path)
    print(f"Video dosyası kaydedildi: {video_path}")
    
    # Transkript çıkar
    transcription = process_video_transcription(video_path)
    print(f"Çıkarılan transkript: {transcription}")
    
    # Video dosyasını sil
    os.remove(video_path)
    print(f"Video dosyası silindi: {video_path}")
    
    # Sonucu döndür
    return jsonify({"transcription": transcription}), 200
