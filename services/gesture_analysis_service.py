import cv2
import mediapipe as mp

def analyze_gestures(video_path):
    """Videodaki yüz ifadelerini ve jestleri analiz eder"""
    
    # Mediapipe ve OpenCV yapılandırması
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

    # Video yakalama
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    gesture_data = []

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame_count += 1

        # BGR'den RGB'ye çevir
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Yüz analizini yap
        results = face_mesh.process(frame_rgb)

        # Jest ve mimik tespiti
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Göz açıklığı ve ağız hareketi gibi bazı jestleri tespit et
                try:
                    eye_openness = face_landmarks.landmark[145].y - face_landmarks.landmark[159].y
                    mouth_openness = face_landmarks.landmark[13].y - face_landmarks.landmark[14].y

                    # Jest verilerini kaydet
                    gesture_data.append({
                        "frame": frame_count,
                        "eye_openness": eye_openness,
                        "mouth_openness": mouth_openness
                    })

                except IndexError as e:
                    print(f"Yüz analizinde hata: {str(e)}")
                    continue

    # Kaynakları serbest bırak
    cap.release()
    face_mesh.close()

    # Analiz sonucunu döndürmeden önce veriyi kontrol et
    if len(gesture_data) == 0:
        print("Hiçbir jest verisi tespit edilmedi.")
    else:
        print(f"Toplam jest verisi: {len(gesture_data)} kare")

    return gesture_data
