'''
capture.py -- Image capture tool for YOLO dataset collection
Streams a live camera feed and saves clean JPEG frames to a captures/ folder
when the user presses SPACE. This is the first step in a YOLO training data
collection pipeline.

HOW TO USE
----------
1. Set START_NUMBER if you want numbering to continue from a previous session.
2. Set the camera index in cv2.VideoCapture() to match your device.
3. Run:  python capture.py
4. Press SPACE to save the current frame. Press Q to quit.

Images are saved as img_000.jpg, img_001.jpg, etc. inside the captures/ folder
next to this file.
'''

# region Imports
import cv2
import os
# endregion Imports

# region Configuration
START_NUMBER  = 0        # Change this to continue numbering from a previous session
OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "captures")
# endregion Configuration

# region Camera Setup
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

counter = START_NUMBER

cap = cv2.VideoCapture(4)  # Change this index to match your camera device

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

print("Camera opened. Press SPACE to capture. Press 'q' to quit.")
# endregion Camera Setup

# region Main Loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    # Draw overlay on a copy so the saved image stays clean
    display = frame.copy()
    label = f"Next: img_{counter:03d}.jpg  |  SPACE to capture  |  Q to quit"
    cv2.putText(display, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow("Camera Feed", display)

    key = cv2.waitKey(1) & 0xFF

    if key == ord(' '):
        filename = os.path.join(OUTPUT_FOLDER, f"img_{counter:03d}.jpg")
        cv2.imwrite(filename, frame)  # saves the clean frame, not the display overlay
        print(f"Saved: {filename}")
        counter += 1
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(f"Done. {counter - START_NUMBER} image(s) saved to '{OUTPUT_FOLDER}/'.")
# endregion Main Loop
