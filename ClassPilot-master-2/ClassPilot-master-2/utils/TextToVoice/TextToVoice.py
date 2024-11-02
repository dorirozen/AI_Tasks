from gtts import gTTS
import os
import pygame

DIR_PATH = os.path.abspath(os.path.curdir)

class MP3Player:
    def __init__(self):
        pygame.mixer.init()

    def play(self, file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
    def is_playing(self):
        return pygame.mixer.music.get_busy()

class TextToVoice:
    def __init__(self,name="output"):
        self.audio_file = f"{name}.mp3"
        self.play_obj = MP3Player()

    def generate_speech(self, text, lang='en', tld='com', slow=False, lang_check=True, name=None):
        tts = gTTS(text=text, lang=lang, tld=tld, slow=slow, lang_check=lang_check)
        if name is None:
            name = 'output'
        self.audio_file = DIR_PATH + f"\\{name}.mp3"
        tts.save(self.audio_file)
    def is_playing(self) -> bool:
        return self.play_obj.is_playing()
    def play(self, text, lang='en'):
        self.generate_speech(text, lang=lang)
        if self.play_obj.is_playing():
            self.play_obj.stop()
        self.play_obj.play(self.audio_file)
        self.remove()

    def stop(self):
        if self.play_obj.is_playing():
            self.play_obj.stop()
        self.remove()

    def remove(self):
        try:
            while self.play_obj.is_playing():
                pass
            self.play_obj.stop()
            os.remove(self.audio_file)
        except Exception as e:
            print(e)




