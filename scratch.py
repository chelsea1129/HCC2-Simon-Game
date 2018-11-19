
import datetime
from playsound import playsound
import threading

soundpath="audio/bleep.wav"

print(datetime.datetime.now())
print(datetime.datetime.now())

t1 = threading.Thread(target=playsound, args=[soundpath])
t1.start()

#playsound(soundpath)

print(datetime.datetime.now())
