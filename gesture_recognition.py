import mediapipe as mp
import time
import cv2

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

def on_result(result, output_image: mp.Image, timestamp_ms: int):
    #print(f"Gestures at {timestamp_ms} ms: {result.gestures}")
    if len(result.gestures) == 2:
        gesture1 = result.gestures[0][0].category_name
        gesture2 = result.gestures[1][0].category_name
        if gesture1 == "Open_Palm":
            if gesture2 == "Victory":
                print('hand 1 lose')
            elif gesture2 == "Closed_Fist":
                print('hand 1 win')
            else:
                print('tie')
        elif gesture1 == "Victory":
            if gesture2 == "Closed_Fist":
                print('hand 1 lose')
            elif gesture2 == "Open_Palm":
                print('hand 1 win')
            else:
                print('tie')
        else:
            if gesture2 == "Closed_Fist":
                print('tie')
            elif gesture2 == "Open_Palm":
                print('hand 1 lose')
            else:
                print('hand 1 win')

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path="gesture_recognizer.task"),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=2,
    result_callback=on_result,
)

def stream_webcam(recognizer: mp.tasks.vision.GestureRecognizer, camera_index: int = 0):
    cap = cv2.VideoCapture(camera_index)
    try:
        while cap.isOpened():
            ok, bgr_frame = cap.read()
            if not ok:
                break
            rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            timestamp_ms = time.monotonic_ns() // 1_000_000
            recognizer.recognize_async(mp_image, timestamp_ms)
            cv2.imshow("Webcam", bgr_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

with GestureRecognizer.create_from_options(options) as recognizer:
    stream_webcam(recognizer)