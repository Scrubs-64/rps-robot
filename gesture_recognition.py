import mediapipe as mp
import time
import cv2
import random

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

class GestureRecognition:
    def __init__(self):
        self.gest_list = ['Open_Palm', 'Closed_Fist', 'Victory']
        self.machine_play = random.choice(self.gest_list)
        self.hand_lowered = False
        self.locked_gesture = None
        self.current_gesture = None
        self.mode = None
        self.start = None

        self.options = GestureRecognizerOptions(
            base_options=BaseOptions(
                model_asset_path="gesture_recognizer.task"
            ),
            running_mode=VisionRunningMode.LIVE_STREAM,
            num_hands=2,
            result_callback=self.on_result
        )
        

    def on_result(self, result, output_image: mp.Image, timestamp_ms: int):
        #print(f"Gestures at {timestamp_ms} ms: {result.gestures}")
        match self.mode:
            case 'pump':
                if not(result.hand_landmarks == []):
                    #print(result.hand_landmarks[0][0])
                    if result.hand_landmarks[0][0].y > 0.5:
                        #print('yes')
                        if self.hand_lowered == False:
                            print('hand lowered')
                        self.hand_lowered = True
                    else:
                        if self.hand_lowered == True:
                            print('hand raised')
                        self.hand_lowered = False
                    #for i in range(0, len(result.hand_world_landmarks[0])):
                    #    print(result.hand_world_landmarks[0][i])
            case 'lock_in':
                if result.gestures != []:
                    gesture = result.gestures[0][0].category_name
                    #print(gesture)
                    if self.current_gesture == None:
                        self.current_gesture = gesture
                    elif self.current_gesture != gesture:
                        self.start = time.monotonic()
                        self.current_gesture = gesture
                        print('change detected')
                    elif self.current_gesture == gesture and time.monotonic() - self.start >= 2 and gesture != None:
                        self.current_gesture = gesture
                        self.locked_gesture = gesture
                    
        
        global machine_play
        """ if len(result.gestures) == 2:
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
        elif len(result.gestures) == 1:
            print('machine plays ' + machine_play)
            gesture = result.gestures[0][0].category_name
            if gesture == "Closed_Fist":
                if machine_play == "Closed_Fist":
                    print('tie')
                elif machine_play == "Open_Palm":
                    print('human lose')
                else:
                    print('human win')
                    machine_play = gest_list[random.randint(0, 2)]

            elif gesture == "Open_Palm":
                if machine_play == "Victory":
                    print('human lose')
                elif machine_play == "Closed_Fist":
                    print('human win')
                    machine_play = gest_list[random.randint(0, 2)]
                else:
                    print('tie')
            else:
                if machine_play == "Victory":
                    print('tie')
                elif machine_play == "Closed_Fist":
                    print('human lose')
                else:
                    print('human win')
                    machine_play = gest_list[random.randint(0, 2)] """
        
    def stream_webcam(self, recognizer: mp.tasks.vision.GestureRecognizer, camera_index: int = 0):
        cap = cv2.VideoCapture(camera_index)
        self.start = time.monotonic()
        last_timestamp_ms = -1
        try:
            while cap.isOpened() and self.locked_gesture == None:
                ok, bgr_frame = cap.read()
                if not ok:
                    break
                rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
                timestamp_ms = time.monotonic_ns() // 1_000_000
                timestamp_ms = max(timestamp_ms, last_timestamp_ms + 1)
                last_timestamp_ms = timestamp_ms
                recognizer.recognize_async(mp_image, timestamp_ms)
                cv2.imshow("Webcam", bgr_frame)
                #time.sleep(0.5)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        finally:
            print('locked gesture: ' + self.locked_gesture)
            cap.release()
            cv2.destroyAllWindows()

    def read_gesture(self):
        self.mode = 'lock_in'
        with GestureRecognizer.create_from_options(self.options) as recognizer:
            self.stream_webcam(recognizer)

        return self.locked_gesture
    def pumping