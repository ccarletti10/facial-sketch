import cv2

# Create a VideoCapture object for the default camera (camera ID 0)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
exit()

# Wait for a key press to capture the image
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Display the frame (optional, for preview)
    cv2.imshow("Camera Preview", frame)

    # Wait for a key press (e.g., 'c' or 'q') to capture or quit
    key = cv2.waitKey(1) & 0xFF # Use bitwise AND to handle different systems
    if key == ord('c'):
    # Capture the image
        cv2.imwrite("captured_image.jpg", frame)
        print("Image captured and saved as captured_image.jpg")
        break # Exit the loop after capturing

    elif key == ord('q'):
    # Quit the program
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()