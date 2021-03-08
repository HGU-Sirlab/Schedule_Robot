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

#함수화가 필요할 수도 있어보이긴한다...
#우선 코드를 다 짜고 정리하

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
  name = 'James'
  team = 'sirlab'
  schedule = [1,1,1]
  schedule_motion = [1,1,1]
  schedule_motion = [1,1,1]
  schedule_motion = [1,1,1]

  while True: #프로그램이 죽지 않도록 전체 코드 반복

    #<영상> 얼굴인식 대기(1초단위)
    while True: #영상인식 대기를 위한 반복
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

    if name == "Guest"  : # 게스트
        print("게스트")

    elif name == "한재" : # 교수님
        #<TTS>"안녕하세요. 교수님 오늘도 연구실은 제가 잘 지키고 있습니다 ㅎㅎ"
        tObj.tts("<speak>\
                <voice name='MAN_READ_CALM'> 안녕하세요. 교수님 오늘도 연구실은 제가 잘 지키고 있습니다 ㅎㅎ </voice>\
                  </speak>"\
                , filename)
        #<모션> 댄스
        m.set_motion(name="right_side",cycle=1)
        time.sleep(2)

        #<파일> 일정가져오기
        with open('schedule.pickle','rb') as fr:
            schedule_loaded = pickle.load(fr)
        schedule_motion = schedule_loaded["motion"]
        schedule_security = schedule_loaded["security"]
        schedule_avatar = schedule_loaded["avartar"]

        schedule_motion = 'NONE'
        schedule_security = 'NONE'
        schedule_avatar = 'NONE'

        #일정이 없다면
        if schedule_motion == 'NONE'  and schedule_security == 'NONE' schedule_avatar == 'NONE':
            #<TTS> "오늘 예정된 미팅은 없습니다."
            tObj.tts("<speak>\
                    <voice name='MAN_READ_CALM'> 오늘 계획되어 있는 일정은 없습니다. </voice>\
                    </speak>"\
                    , filename)

        #일정이 있다면
        else :
            #<TTS> "XX팀 XX시 미팅있습니다." for 문 사용해야할
            tObj.tts("<speak>\
                    <voice name='MAN_READ_CALM'> XX팀 XX시 미팅있습니다. </voice>\
                    </speak>"\
                    , filename)

        #<TTS> "좋은 하루 되세요 교수님"
        tObj.tts("<speak>\
                <voice name='MAN_READ_CALM'> 좋은 하루 되세요! 교수님! </voice>\
                </speak>"\
                , filename)

    else # 연구원

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
        with open('user.pickle','rb') as fr:
            user_loaded = pickle.load(fr)
        team = user_loaded[name]

        #<파일>i일정!에서 일정 정보 가져오기
        with open('schedule.pickle','rb') as fr:
            schedule_loaded = pickle.load(fr)
        schedule = schedule_loaded[team]

        #<TTS>"**팀 오늘 **시 미팅 있습니다. 일정을 추가할까요?"
        tObj.tts("<speak>\
                <voice name='MAN_READ_CALM'>"+team+"팀 오늘"+schedule[1]+"시 미팅 있습니다. 일정을 추가할까요? </voice>\
                  </speak>"\
                , filename)

        aObj.play(filename, out='local', volume=-500)
        time.sleep(10)


        #<STT> "Yes" or "No" 인식하기
        ret = tObj.stt()
        if('Yes' in ret or '네' in ret):
            print("going")

        else :
            #<TTS> "입력이 완료되었습니다."
            tObj.tts("<speak>\
                    <voice name='MAN_READ_CALM'> 알겠습니다!  좋은하루 되세요! </voice>\
                      </speak>"\
                     , filename)

            aObj.play(filename, out='local', volume=-500)
            time.sleep(2)
            #<모션> 마지막 인사
            m.set_motion(name="byebye",cycle=1)
            time.sleep(2)
            continue

        #print(" #<STT2> Yes or No 인식하기")
        time.sleep(1)


        #<LED> 음량정보,남은시간 표시
        #print("#<LED> 음량정보,남은시간 표시")
        #time.sleep(1)

        #<STT> "**일 **시"
        #print("#<STT> **일 **시")
        month = 9
        date = 10
        hour = 12
        time_schedule =[month,date,hour]
        time.sleep(1)

        #<LED> 음량정보,남은시간 표시
        #print("#<LED> 음량정보,남은시간 표시")
        #time.sleep(1)

        #<파일>i일정!에 저장
        schedule_load[team] = time_schedule
        with open('schedule.pickle','wb') as fw:
            pickle.dump(scheduel_load,fw)

        #print("#<파일>i일정!에 저장")
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
