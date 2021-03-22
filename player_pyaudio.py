import sounddevice as sd
import soundfile as sf
import threading
from threading import Thread
import convert
import os
import time
class player(threading.Thread):
    def __init__(self,audio,deviceid):
        super().__init__()
        self.audio=audio
        self.device=deviceid
        self.playing=True
    def check(self,audio):
        if audio[-3]!="wav":
            t=convert.convert_mp3_to_wav(audio)
            found=False
            for root, dirs, files in os.walk("temp", topdown=False):
                for file in files:
                    if file==(t.name+".wav"):
                        found=True
                        break
            if found:
                self.audio=t.dst
            else:
                t.start()
                self.audio=t.dst
                time.sleep(2)
    def run(self):
        self.check(self.audio)
        self.t2=Thread(target=self.audio_play,args=(self.audio,self.device,))
        self.t2.start()
    def audio_play(self,audio,deviceid):
        data1, fs1 = sf.read(audio, dtype='float32')
        sd.play(data1, fs1, device=deviceid,blocking=True)
    def stop(self):
        sd.stop()
if __name__=="__main__":
    p=player("default\\hello there.mp3",5,8).start()