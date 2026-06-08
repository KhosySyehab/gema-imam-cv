import cv2
import mediapipe as mp

# Di Python 3.11, pemanggilan ini akan berjalan dengan mulus
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Buka kamera bawaan, TAPI paksa menggunakan backend V4L2 milik Linux
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# Set properti untuk meringankan beban WSL
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# TAMBAHAN BARU: Paksa buffer size menjadi 1 agar frame tidak menumpuk dan macet
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not cap.isOpened():
    print("ERROR: Tidak bisa membuka kamera. Pastikan usbipd sudah ter-attach dan permission /dev/video sudah dibuka.")
    exit()

print("Memproses video... Tekan 'q' di keyboard untuk keluar.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Gagal menangkap frame dari kamera.")
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
        )

    cv2.imshow('Prototipe GEMA Imam - WSL Mode', frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()