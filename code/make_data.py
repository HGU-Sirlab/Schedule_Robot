# -*- coding: UTF-8 -*-
  
import pickle

user = {'김준희' : 'motion','최지환':'motion','김명섭':'motion', '배한재':'Security'}    
schedule = {'motion':[10,2,15],'Security' : [3, 2, 10]}
         
with open('user.pickle','wb') as fw:
    pickle.dump(user,fw)
with open('schedule.pickle','wb') as fw:
    pickle.dump(schedule,fw)
