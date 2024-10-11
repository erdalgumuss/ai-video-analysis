import os
from flask import request, jsonify
from services.transcription_service import process_video_transcription
from services.gesture_analysis_service import analyze_gestures


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

def analyze_video_gestures():
    # Fonksiyonun çağrıldığını doğrulamak için bir mesaj yazalım
    print("analyze_video_gestures() fonksiyonu çağrıldı.")

    # Kullanıcının yüklediği video dosyasını al
    if 'video' not in request.files:
        print("Hata: Video dosyası sağlanmadı.")
        return jsonify({"error": "No video file provided"}), 400
    
    video_file = request.files['video']
    video_path = f"./uploads/{video_file.filename}"
    
    # 'uploads' klasörünün var olup olmadığını kontrol et ve yoksa oluştur
    if not os.path.exists('./uploads'):
        os.makedirs('./uploads')
    
    # Video dosyasını sunucuda geçici olarak kaydet
    video_file.save(video_path)
    print(f"Video dosyası kaydedildi: {video_path}")
    
    # Jest ve mimik analizini yap
    print("Jest ve mimik analizi başlatılıyor...")
    gesture_data = analyze_gestures(video_path)
    
    # Eğer gesture_data boşsa, bir hata döndürelim
    if not gesture_data:
        print("Hiçbir jest verisi tespit edilmedi.")
        return jsonify({"error": "No gesture data detected"}), 400
    
    # Video dosyasını sil
    os.remove(video_path)
    print(f"Video dosyası silindi: {video_path}")
    
    # Sonucu döndür
    return jsonify({"gesture_analysis": gesture_data}), 200
