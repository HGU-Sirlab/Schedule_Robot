import os
import sys
import time

# 상위 디렉토리 추가 (for utils.config)
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utils.config import Config as cfg

# openpibo 라이브러리 경로 추가
sys.path.append(cfg.OPENPIBO_PATH + '/lib')
from vision.visionlib import cCamera
from vision.visionlib import cFace
from speech.speechlib import cSpeech
from audio.audiolib import cAudio
from motion.motionlib import cMotion

def test_f():
  # instance
  cam = cCamera()
  faceObj = cFace(conf=cfg)
  faceObj.load_db("facedb")
  print(faceObj.get_db()[0])
  
  tObj = cSpeech(conf=cfg)
  filename = cfg.TESTDATA_PATH+"/tts.mp3"

  aObj = cAudio()

  m = cMotion(conf=cfg)
  
  while True:
    while True:
      # Capture / Read file
      img = cam.read()
      print("cheeze")
      #img = cam.imread("/home/pi/test.jpg")
 
      # detect faces
      faceList = faceObj.detect(img)

      if len(faceList) >= 1:
        break
      else :
        print("No face")
        time.sleep(1)

    # recognize using facedb
    ret = faceObj.recognize(img, faceList[0])
    name = "Guest" if ret == False else ret["name"]
    
    tObj.tts("<speak>\
            <voice name='MAN_READ_CALM'>"+name+"님 안녕하세요. </voice>\
              </speak>"\
            , filename)

    aObj.play(filename, out='local', volume=-500)
    m.set_motion(name="hello",cycle=1) 
    time.sleep(2)


if __name__ == "__main__":
  test_f()

