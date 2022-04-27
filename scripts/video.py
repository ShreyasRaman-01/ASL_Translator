'''Video Capturing: head/start of program execution + UI/UX handler'''
import cv2
from config import Configs
import pdb
from screeninfo import get_monitors
import pyttsx3

class aslTranslator:

    def __init__(self):

        self.video_capture = cv2.VideoCapture(0)
        self.configs = Configs
        self.voice_engine = pyttsx3.init()

        #set initial voice
        self.updateVoice(self.configs.CHOSEN_VOICE)

    def updateRate(self, rate_delta):
        rate = self.voice_engine.getProperty('rate')
        self.voice_engine.setProperty('rate', rate+rate_delta)


    def updateVol(self, vol_delta):
        volume = self.voice_engine.getProperty('volume')
        self.voice_engine.setProperty('volume', volume-vol_delta)

    def updateVoice(self, new_voice):

        voice_idx = self.configs.VOICE_OPTIONS[new_voice]
        voices = self.voice_engine.getProperty('voices')
        self.voice_engine.setProperty('voice', voices[voice_idx])


    def run_video(self):

        print('Starting application...')

        WINDOW_NAME = self.configs.WINDOW_NAME

        ___, sample_frame = self.video_capture.read()
        new_width, new_height = self.get_scaling_factors(sample_frame.shape)


        monitors = get_monitors()
        screen_width, screen_height = monitors[0].width, monitors[0].height

        while (True):

            #capture frames of video
            # try:
            ret, frame = self.video_capture.read()

            output = 'the quick brown fox jumped over'


            #generate class prediction on frame


            # display frame
            cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

            #resize frame to desired size
            # frame = cv2.resize(frame, (new_width*2,new_height*2), interpolation = cv2.INTER_AREA)

            #display text/visuals on frame
            cv2.rectangle(frame, (0, frame.shape[0] - self.configs.BG_HEIGHT), (frame.shape[1], frame.shape[0]), self.configs.BG_COLOR, -1)

            if self.configs.TOGGLE_TEXT:
                cv2.putText(frame, output.upper(), (self.configs.TEXT_OFFSET[1], frame.shape[0] - self.configs.TEXT_OFFSET[0]), self.configs.FONT,self.configs.FONT_SCALE, self.configs.FONT_COLOR, self.configs.LINE_THICKNESS, self.configs.LINE_TYPE)

            cv2.imshow(WINDOW_NAME, frame)

            #generate voiceover
            if self.configs.TOGGLE_VOICE:
                self.voice_engine.say(output)
                self.voice_engine.runAndWait()



            #check for quit signal
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


            # except:
            #     raise Exception('Error: could not load video capture')


        print('Quit Program: exiting application ....')
        self.video_capture.release()
        cv2.destroyAllWindows()

    def get_scaling_factors(self, frame_shape):

        frame_height, frame_width, _ = frame_shape

        monitors = get_monitors()
        screen_width, screen_height = monitors[0].width, monitors[0].height

        scaleWidth = float(screen_width)/float(frame_width)
        scaleHeight = float(screen_height)/float(frame_height)

        imgScale = scaleWidth if scaleWidth < scaleHeight else scaleHeight

        new_width, new_height = int(frame_width*imgScale), int(frame_height*imgScale)

        return new_width, new_height


    def test_text_to_voice(self):
        voices = self.voice_engine.getProperty('voices')
        for i,voice in enumerate(voices):
            if voice.languages[0].split('_')[0] == u'en':
                self.voice_engine.setProperty('voice', voice.id)
                self.voice_engine.say('Hello World')
                self.voice_engine.runAndWait()



test = aslTranslator()
# test.test_text_to_voice()
test.run_video()
