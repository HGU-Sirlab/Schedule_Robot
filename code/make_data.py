# -*- coding: UTF-8 -*-
  
import pickle

user = {'준희' : 'motion','지환':'motion','명섭':'motion', '한재':'Security'}    
schedule = {'motion':['2','15'],'Security' : ['2', '10']}
         
with open('user.pickle','wb') as fw:
    pickle.dump(user,fw)
with open('schedule.pickle','wb') as fw:
    pickle.dump(schedule,fw)
