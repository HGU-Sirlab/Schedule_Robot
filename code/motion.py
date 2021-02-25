# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 16:45:10 2021

@author: sirlab
"""
import os
import sys
import time

import socket
import numpy as np

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
    
    #<모션> 오른손 인사
    m.set_motion(name="hello",cycle=1) 
    time.sleep(1)

    
    #<모션> 마지막 인사
    m.set_motion(name="byebye",cycle=1) 
    time.sleep(2)

    #반복문 다시 처음으로…
    print("#반복문 다시 처음으로…")

def sock():
    ## TCP 사용
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ## server ip, port
    s.connect(('192.168.0.30', 5001))
    return s

def run(conn):
    m = cMotion(conf=cfg)
    data = conn.recv(1024)
    if not data:
        print("Empty Data")
    else:
        print('Received from', data.decode())
    
    if(data.decode() == "hello"):
        m.set_motion(name="hello",cycle=1) 
        time.sleep(1)
    
if __name__ == "__main__":
    conn = sock()
    run(conn)
    #test_f()
