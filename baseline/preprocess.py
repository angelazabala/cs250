import email
import enchant
import re
import os

dictionary = enchant.Dict("EN-US")

def get_eng_words(content_array, mail):
    filtered = open("data2"+mail[4:], "w")

    for i in content_array:
        try:
            i = i.upper()
        except:
            continue

        if(i=="FONT-SIZE" or i=="THREAD-INDEX" or i=="COM" or i=="ID" or len(i)==1):
            continue
        elif(i=="SUN" or i=="THU" or i=="SAT" or i=="WED" or i=="MON" or i=="TUE" or i=="FRI"):
            continue
        elif(i=="APR" or i=="JAN" or i=="FEB" or i=="MAR" or i=="JUN" or i=="OCT" or i=="SEP" or i=="AUG" or i=="NOV" or i=="DEC" or i=="JUL"):
            continue
        elif(len(i)==2):
            if(i[0]=='A' or i[0]=='E' or i[0]=='I' or i[0]=='O' or i[0]=='U'):
                if(i[1]=='A' or i[1]=='E' or i[1]=='I' or i[1]=='O' or i[1]=='U'):
                    continue
            elif(i[1]!='O' and i[1]!='F' and i[1]!='P' and i[1]!='N' and i[1]!='T' and i[1]!='M' and i[1]!='E' and i[1]!="X"):
                continue
        else:
            if(dictionary.check(i)):
                filtered.write(i+" ")

    filtered.close()



def clean_email(mail):
    raw_email = open(mail, "r", encoding="ISO-8859-1")
    str_email = str(raw_email.read())
    processed = re.sub(r'(List-|Precedence:|Resent-|for <|Content|Lines|Return|Delivered|Mailing-|Thread-|Mail-|RT-|Status:|Received|Old-|User-|Message-|Reply-|To:|Subject|Date:|X-Mailer|MIME|Mime|X-|Status|From).*\n', r' ', str_email)
    processed = re.sub(r'(by speedy|by murphy|by xenon|by net|by cess|version=|boundary=|by pl|smtp|MIME-).*\n', r' ', processed)
    processed = re.sub(r'This is a multi-part message in MIME format.', r' ', processed)
    processed = re.sub(r'id [0-9].*\n', r' ', processed)
    processed = re.sub(r'[0-9]*-*[0-9]+-*', r' ', processed)
    processed = re.sub(r'</*span>', r'', processed)
    processed = re.sub(r'<style>.*</style>', r' ', processed)
    processed = re.sub(r'<[^>]+>', r' ', processed)
    processed = re.sub(r'(http[s]*:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', r' ', processed)
    processed = re.sub(r'-+', r'', processed)
    processed = re.sub(r'[^A-Za-z ]', r' ', processed)
    processed = re.sub(r'\s+', r' ', processed)
    
    words=processed.split()

    get_eng_words(words, mail)

def preprocess():
    if not os.path.exists("data2/"):
        os.makedirs("data2/")

    for i in range(1,75420):
        print("Preprocessing data/inmail."+str(i))
        clean_email("data/inmail."+str(i))