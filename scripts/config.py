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
    CLASS_IDX = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G',
    7:'H', 8:'I', 9:'J', 10:'K', 11:'L', 12:'M', 13:'N', 14:'O', 15:'P',
    16:'Q', 17:'R', 18:'S', 19:'T', 20:'U', 21:'V', 22:'W', 23:'X', 24:'Y', 25:'Z', 26: '', 27:'space', 28:'speak'}
