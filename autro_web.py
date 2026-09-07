'''
--------------------------------------------------------
             LAMA CHATBOT
             --------------------------
____________________________________
'''
import requests
import time 
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
data={'hi':'hello'}            
while True:
    x=str(input('MY MASSAGE IS :---->'))
    if x.lower() in list(data.keys()):
        time.sleep(3)
        print(data[x])
    else:
        print('please bro that information in not in my data ,can add it °_° please ')   
        time.sleep(1) 
        print('\n write [yes] if you want it.\n write [no] if dont want it '.center(60).upper())
        v=input('your reply :   ')
        if v.lower()=='yes':
            b=str(input('your reponse of your quoition is : '))
            v.append(list(data))
            v.append(list(data))
            print(data)
            time.sleep(2)
            print('thanks bro  I LOVE YOU ')
        else:
             time.sleep(2)   
             print('no worre bro ,just thanks bro \n if you nead help Im hear for you ^-^')
             