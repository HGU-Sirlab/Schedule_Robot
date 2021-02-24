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
  print(faceObj.get_db()[0]) #DB 업데이트 확인용  
  tObj = cSpeech(conf=cfg)
  filename = cfg.TESTDATA_PATH+"/tts.mp3" #tObj 관련 파일명 변수
  aObj = cAudio()
  m = cMotion(conf=cfg)
  
  #variable
  name = "디폴트"
  team = "디폴트"
  schedule = ("디폴트", "디폴트")

  while True:
    
    #<영상> 얼굴인식 대기(1초단위)
    while True:
      # Capture / Read file
      img = cam.read()
      print("cheeze") #촬영확인용
 
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
    
    #<TTS>"**님 안녕하세요"
    tObj.tts("<speak>\
            <voice name='MAN_READ_CALM'>"+name+"님 안녕하세요. </voice>\
              </speak>"\
            , filename)

    aObj.play(filename, out='local', volume=-500)
    
    #<모션> 오른손 인사
    m.set_motion(name="hello",cycle=1) 
    time.sleep(1)

    #<파일>i팀정보!에서 무슨 팀인지 가져오기
    #<파일>i일정!에서 일정 정보 가져오기
    
    #<TTS>"**팀 오늘 **시 미팅 있습니다. 일정을 추가할까요?"
    tObj.tts("<speak>\
            <voice name='MAN_READ_CALM'>"+team+"팀 오늘"+schedule[1]+"시 미팅 있습니다. 일정을 추가할까요? </voice>\
              </speak>"\
            , filename)

    aObj.play(filename, out='local', volume=-500)
    time.sleep(2)


    #<STT> "Yes" or "No" 인식하기
    print(" #<STT2> Yes or No 인식하기")
    time.sleep(1)

    
    #<LED> 음량정보,남은시간 표시
    print("#<LED> 음량정보,남은시간 표시")
    time.sleep(1)

    #<STT> "**일 **시"
    print("#<STT> **일 **시")
    time.sleep(1)

    #<LED> 음량정보,남은시간 표시
    print("#<LED> 음량정보,남은시간 표시")
    time.sleep(1)

    #<파일>i일정!에 저장
    print("#<파일>i일정!에 저장")
    time.sleep(1)

    #<TTS> "입력이 완료되었습니다."
    tObj.tts("<speak>\
            <voice name='MAN_READ_CALM'> 입력이 완료되었습니다. 연구시작하세요! </voice>\
              </speak>"\
            , filename)

    aObj.play(filename, out='local', volume=-500)
    time.sleep(2)

    #<모션> 마지막 인사
    m.set_motion(name="byebye",cycle=1) 
    time.sleep(2)

    #반복문 다시 처음으로...
    print("#반복문 다시 처음으로...")


if __name__ == "__main__":
  test_f()

