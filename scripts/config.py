import cv2

class Configs:

    #video text/font configurations
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONT_COLOR = (255,255,255)
    LINE_TYPE = cv2.LINE_4
    LINE_THICKNESS = 3
    FONT_SCALE = 1

    TEXT_OFFSET = (20,20)

    #black background to text
    BG_COLOR = (0,0,0)
    BG_HEIGHT = 50


    WINDOW_NAME = 'ASL Translator'

    #options within program
    TOGGLE_VOICE = True
    TOGGLE_TEXT = True

    #options for voice
    VOICE_OPTIONS = {'US Male 1': 0, 'UK Male': 7, 'US Male 2': 11, 'AUS Female 1': 17, 'IRE Female 1': 28, 'IND Male 1': 32,\
                    'US Female 1': 33, 'NZ Female 1':37, 'IND Female 1':40, 'US Female 2':41}
    CHOSEN_VOICE = 'US Male 1'
    SPEED_DELTA = 20
    VOL_DELTA = 0.2

    #model configs: number of classes + LR etc...

    # 26 letters + no hand + space + speak 
    NUM_CLASSES = 26 + 3
