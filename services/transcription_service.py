import speech_recognition as sr
from moviepy.editor import VideoFileClip
import os

def extract_audio_from_video(video_path, audio_path):
    """Videodan ses çıkar ve bir dosyaya kaydet"""
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    video.close()

def transcribe_audio(audio_path):
    """Ses dosyasını metne dönüştür"""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        print("Ses verisi alındı, tanıma işlemi başlıyor.")
        try:
            text = recognizer.recognize_google(audio_data, language='tr-TR')
            print(f"Tanımlanan metin: {text}")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition sesi anlayamadı.")
            return None
        except sr.RequestError as e:
            print(f"Google Speech Recognition hizmetine erişim başarısız oldu; {e}")
            return None


def process_video_transcription(video_path):
    """Video dosyasını işleyerek transkript çıkar"""
    audio_path = "temp_audio.wav"
    
    try:
        # Videodan ses çıkar
        extract_audio_from_video(video_path, audio_path)
        
        # Sesi metne dönüştür
        transcription = transcribe_audio(audio_path)
        
        if not transcription:
            print("Transcription boş değer döndü!")
            return "Transcription failed"
        
        return transcription
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return f"Hata: {str(e)}"
    finally:
        # Geçici ses dosyasını sil
        if os.path.exists(audio_path):
            os.remove(audio_path)
