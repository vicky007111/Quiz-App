import jwt
from datetime import datetime,date
import os
from os import path
from dotenv import load_dotenv
from flask import render_template

token_secret_key = os.environ.get("TOKEN_SECRET_KEY")

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(path.join(basedir,".env"))

def generate_token(userId,expires=600):
    reset_token = jwt.encode(
        {"payload":f"{userId}",
         "exp":datetime.datetime.now(tz=datetime.timezone.utc)+datetime.timedelta(seconds=expires)},
         token_secret_key,
         algorithm="HS256")
    return reset_token

def verify_token(token,userId):
    data = jwt.decode(token,token_secret_key,leeway=datetime.timedelta(seconds=20),algorithms=["HS256"])
    if data['payload'] == str(userId):
        return True
    if jwt.ExpiredSignatureError:
        return False

def create_report(name,class_and_sec,testCode,regno,status,score,percentage,lab_session,audio_no,file):
    today = date.today()
    now = datetime.now()
    todays_date = today.strftime("%d %B %Y")
    todays_time = now.strftime("%H:%M %p")
    template = render_template(f"{file}",name=name,Class=class_and_sec,TestCode=testCode,regno=regno,status=status,score=score,percentage=percentage,time=todays_time,Date=todays_date,lab_session=lab_session,audio_no=audio_no)
    return template


def create_csv(filename,report_details):
    import csv
    fields = ['name','score','percentage','status']
    with open(os.path.join(os.path.abspath("admin_reports"),filename),"w+") as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=fields)
        writer.writeheader()
        writer.writerows(report_details)