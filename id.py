import cv2
import face_recognition
import getpass  # For secure password input

# Store user data (ID, password, face encoding)
user_data = {}

def register_user(person_id, password, image_path):
    """Registers a user with an ID, password, and image encoding from a single picture."""
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)

    if len(encoding) == 0:
        print("❌ No face detected in the image. Please use a clear face image.")
        return
    
    user_data[person_id] = {
        "password": password,
        "face_encoding": encoding[0]  
    }
    print(f"✅ User {person_id} registered successfully.")

def authenticate_user(person_id):
    """Authenticates a user by checking the password and verifying the face."""
    if person_id not in user_data:
        print("❌ User not found!")
        return
    
    entered_password = getpass.getpass("🔑 Enter Password: ")  # Secure password input

    if user_data[person_id]["password"] != entered_password:
        print("❌ Incorrect Password! Payment Failed.")
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
            match = face_recognition.compare_faces([user_data[person_id]["face_encoding"]], live_encoding, tolerance=0.5)
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
register_user("12345", "123", "picture.jpg")  # Register user
authenticate_user("12345")  # Authenticate user
