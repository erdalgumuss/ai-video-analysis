import cv2
import mediapipe as mp

# Mediapipe ve OpenCV yapılandırması
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

def analyze_gestures(video_path):
    """Videodaki yüz ifadelerini ve jestleri analiz eder"""
    
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

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                
                # Kaş hareketleri (Kaş kaldırma ve kaş çatma)
                left_brow_height = face_landmarks.landmark[53].y - face_landmarks.landmark[52].y
                right_brow_height = face_landmarks.landmark[282].y - face_landmarks.landmark[283].y
                brow_movement = (left_brow_height + right_brow_height) / 2
                
                # Göz kırpma tespiti (Göz üst ve alt noktaları arasındaki mesafe)
                left_eye_openness = face_landmarks.landmark[145].y - face_landmarks.landmark[159].y
                right_eye_openness = face_landmarks.landmark[374].y - face_landmarks.landmark[386].y
                avg_eye_openness = (left_eye_openness + right_eye_openness) / 2

                # Ağız hareketleri (Gülümseme veya üzgün ifade)
                mouth_width = face_landmarks.landmark[61].x - face_landmarks.landmark[291].x
                mouth_openness = face_landmarks.landmark[13].y - face_landmarks.landmark[14].y

                # Basit jest puanlaması
                gesture_data.append({
                    "frame": frame_count,
                    "brow_movement": brow_movement,
                    "eye_openness": avg_eye_openness,
                    "mouth_width": mouth_width,
                    "mouth_openness": mouth_openness
                })

    cap.release()
    face_mesh.close()

    return gesture_data
