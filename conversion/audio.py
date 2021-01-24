import os
import pyttsx3
from gtts import gTTS
from pydub import AudioSegment,effects
import moviepy.editor as mp

class Convert(object):
    extensions_dict = {'mp3': ".mp3"}
    
    def __init__(self, file_type, path = ""):
        self.tmp_file = ".tmp"
        self.path = path +  "/"
        self.extension = self.extensions_dict.get(file_type,".mp3")

    def video(self,url,file_name):
        video = mp.VideoFileClip(url)
        video.audio.write_audiofile(self.path + file_name + self.extension)

    def tts(self,text,file_name,language='it',speed=1.2,local=True):
        if local:
            tmp_file = self.tmp_file + self.extension
            languages_voices = {'it': "com.apple.speech.synthesis.voice.luca.premium",
             'en-us': "com.apple.speech.synthesis.voice.Alex"}
            engine = pyttsx3.init()
            engine.setProperty('voice', languages_voices.get(language, languages_voices['it']))
            engine.save_to_file(text, self.path + tmp_file)
            engine.runAndWait()
            #Compress file
            if os.path.isfile(self.path + tmp_file) == True:
                sound = AudioSegment.from_file(self.path + tmp_file)
                sound.export(self.path + file_name + self.extension, format = self.extension[1:], parameters=["-ac","2","-ar","24000"])
                os.remove(self.path + tmp_file)
        else:
            tmp_file = self.tmp_file + self.extension
            tts = gTTS(text,lang=language)
            tts.save(self.path + tmp_file)
            #Speedup file
            if os.path.isfile(self.path + tmp_file) == True:
                sound = AudioSegment.from_file(self.path + tmp_file)
                sound = sound.speedup(playback_speed=speed)
                sound.export(self.path + file_name + self.extension, format = self.extension[1:])
                os.remove(self.path + tmp_file)