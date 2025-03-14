import cv2
import face_recognition

# Store user face encoding
user_face_encoding = None

def register_user(image_path):
    """Registers a user by encoding their face from a single image."""
    global user_face_encoding

    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)

    if len(encoding) == 0:
        print("❌ No face detected in the image. Please use a clear face image.")
        return
    
    user_face_encoding = encoding[0]
    print("✅ User registered successfully with face recognition.")

def authenticate_user():
    """Authenticates a user by verifying their face with a live camera feed."""
    if user_face_encoding is None:
        print("❌ No registered face found! Please register first.")
        return

    print("🔍 Please look at the camera for authentication...")

    cap = cv2.VideoCapture(0)  # Open laptop camera
    match_found = False

    for _ in range(10):  # Capture multiple frames for better accuracy
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture image.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
        face_encodings = face_recognition.face_encodings(rgb_frame)

        for live_encoding in face_encodings:
            match = face_recognition.compare_faces([user_face_encoding], live_encoding, tolerance=0.5)
            if match[0]:
                match_found = True
                break
        
        if match_found:
            break

    cap.release()  # Release camera

    if match_found:
        print("✅ Transaction Completed!")
    else:
        print("❌ Payment Failed - Face does not match.")

# Example Usage:
register_user("picture.jpg")  # Register user with a face image
authenticate_user()  # Authenticate user
