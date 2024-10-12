import speech_recognition as sr
from moviepy.editor import VideoFileClip
import os

def extract_audio_from_video(video_path, audio_path):
    """Videodan ses çıkar ve bir dosyaya kaydet"""
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
        video.close()
    except Exception as e:
        print(f"Ses çıkarma işlemi sırasında hata oluştu: {str(e)}")

def transcribe_audio(audio_path):
    """Ses dosyasını metne dönüştür"""
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='tr-TR')
            return text
    except sr.UnknownValueError:
        print("Google Speech Recognition sesi anlayamadı.")
        return None
    except sr.RequestError as e:
        print(f"Google Speech Recognition hizmetine erişilemedi: {str(e)}")
        return None

def process_video_transcription(video_path):
    """Video dosyasını işleyerek transkript çıkar"""
    audio_path = "temp_audio.wav"
    
    try:
        # Videodan ses çıkar
        extract_audio_from_video(video_path, audio_path)
        print("Ses dosyası başarıyla çıkarıldı.")
        
        # Sesi metne dönüştür
        transcription = transcribe_audio(audio_path)
        if transcription is None:
            print("Transkript çıkarılamadı.")
        else:
            print(f"Çıkarılan transkript: {transcription}")
        
        return transcription
    except Exception as e:
        print(f"Transkript işlemi sırasında hata oluştu: {str(e)}")
    finally:
        # Geçici ses dosyasını sil
        if os.path.exists(audio_path):
            os.remove(audio_path)
