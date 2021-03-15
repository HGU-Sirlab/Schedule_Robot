# -*- coding: UTF-8 -*-

import os
import sys
import time
import pickle

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
from speech.speechlib import cDialog
def test_f():
  # instance
  cam = cCamera()
  faceObj = cFace(conf=cfg)
  faceObj.load_db("facedb")
  print(faceObj.get_db()[0]) #DB 업데이트 확인용  
  tObj = cSpeech(conf=cfg)
  dObj = cDialog(conf=cfg)
  filename = cfg.TESTDATA_PATH+"/tts.mp3" #tObj 관련 파일명 변수
  aObj = cAudio()
  m = cMotion(conf=cfg)
  
  #variable
  name = 'James'
  team = 'sirlab'
  schedule = ['1','1']

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
            <voice name='MAN_READ_CALM'>\
            "+name+"님 안녕하세요 </voice>\
            </speak>"\
            , filename)

    aObj.play(filename, out='local', volume=-500)
    
    #<모션> 오른손 인사
    #m.set_motion(name="hello",cycle=1) 
    m.set_motion(name="cheer1",cycle=1)
    time.sleep(1)

    #<파일>i팀정보!에서 무슨 팀인지 가져오기
    with open('user.pickle','rb') as fr:
        user_loaded = pickle.load(fr)
    team = user_loaded[name]
    #<파일>i일정!에서 일정 정보 가져오기
    with open('schedule.pickle','rb') as fr:
        schedule_loaded = pickle.load(fr)
    schedule = schedule_loaded[team]

    #<TTS>"**팀 오늘 **시 미팅 있습니다. 일정을 추가할까요?"
    tObj.tts("<speak>\
            <voice name='MAN_READ_CALM'>"+team+"팀 오늘"+schedule[1]+"시 미팅\
            있습니다. 일정을 추가하고싶나요오오오 </voice>\
              </speak>"\
            , filename)

    aObj.play(filename, out='local', volume=-500)
    time.sleep(15)


    #<STT> "Yes" or "No" 인식하기
    ret = tObj.stt()
    print(ret)
    if('Yes' in ret or '예' in ret or '어' in ret or  '네' in ret or '좋아' in ret):
        print("ok Thank you~!")
    else:
        print("No??")
        print("반복문 다시 처음으로")
        tObj.tts("<speak>\
                <voice name='MAN_READ_CALM'>일정이 없으시군요 감사합니다\
                <break/></voice></speak>", filename)
        aObj.play(filename, out='local', volume=-500)
        print("말씀감사합니다")
        continue

    time.sleep(1)

    
    #<LED> 음량정보,남은시간 표시
    #print("#<LED> 음량정보,남은시간 표시")
    #time.sleep(1)
    #다음회의가 언제인가요?
    print("지금 말합니다.")
    tObj.tts("<speak>\
            <voice name='MAN_READ_CALM'>날짜와 시간을\
            말씀해주세요.예를 들어, 25일 17시.\
            <break/></voice>\
              </speak>"\
            , filename)
    aObj.play(filename, out='local', volume=-500)
    time.sleep(6)
    
    
    #<STT> "**일 **시"
    ret = tObj.stt()
    print(ret)
    #print("#<STT> **일 **시")
    data = dObj.mecab_morphs(ret)
    time.sleep(1)
    print(data)
    date = data[0]
    t = data[2] #sst 인식이 제대로 안되면 data길이가 짧아질 수 있음
    time_schedule =[date,t]
    time.sleep(1)

    #<LED> 음량정보,남은시간 표시
    #print("#<LED> 음량정보,남은시간 표시")
    #time.sleep(1)

    #<파일>i일정!에 저장
    schedule_loaded[team] = time_schedule
    with open('schedule.pickle','wb') as fw:
        pickle.dump(schedule_loaded,fw)

    #print("#<파일>i일정!에 저장")
    time.sleep(1)

    #<TTS> "입력이 완료되었습니다."
    tObj.tts("<speak>\
            <voice name='MAN_READ_CALM'>"+time_schedule[0]+"일"+time_schedule[1]+"시 입력이 완료되었습니다. 연구시작하세요! <break/></voice>\
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
