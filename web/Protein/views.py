#-*- coding: utf-8 -*-
# checking
from django.views.decorators.cache import cache_page
from django.http import HttpResponse,HttpRequest,JsonResponse
from django.template import RequestContext
from django.shortcuts import render,render_to_response
from django.views.decorators import csrf
import glob
import mimetypes
import smtplib,os,time
from email import encoders
from email.message import Message
from email.Header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from Protein.models import Profile
from django.contrib import messages
from Bio.Alphabet import generic_dna
import shlex
from Bio import SeqIO
from django.contrib.sessions.models import Session
import logging
import subprocess
from StringIO import StringIO
from Protein.models import Profile
import os
from django.http import HttpResponseRedirect
from .form import UploadFileForm
import random
from selenium import webdriver
import time
import sys
from django.core.urlresolvers import reverse
import tensorflow as tf
import keras
import numpy as np
import pandas as pd
from numpy import array
from keras.utils import np_utils
from keras.layers import Dense,Dropout,Flatten,Conv2D,AveragePooling2D,MaxPooling2D,Conv3D,AveragePooling3D,LSTM,GRU,Activation,Conv1D,MaxPooling1D
from keras.models import Sequential
from keras.layers.wrappers import TimeDistributed
from keras import optimizers
from keras.models import load_model
import hashlib
euk_one_hot_model = load_model('./model/Euk_one_hot.h5')
prok_one_hot_model = load_model('./model/prok_one_hot.h5')
seq = [6,3,4,1,1,9,12,0,6,12,7,7,1,10,9,6,3,7,2,7,1,14,2,15,12,7,5,6,7,4,3,9]
x_predict = array(seq)
x_predict = x_predict.reshape(1,1,32)
y_label = prok_one_hot_model.predict_classes(x_predict)[0]
y_prob = prok_one_hot_model.predict_proba(x_predict)
y_label = euk_one_hot_model.predict_classes(x_predict)[0]
y_prob = euk_one_hot_model.predict_proba(x_predict)
OUTPUT_LABEL_EN = ['Plasma membrane', 'Cytoplasm', 'Extracell', 'Periplasm', 'Cell wall', 'Cytoskeleton', 'Vacuole', 'Nucleus', 'Mitochondrion']

OUTPUT_LABEL_TW = ['質膜','細胞質','細胞外','胞外質','細胞壁','細胞骨幹','液泡','細胞核','粒線體']
EUK_OUTPUT_LABEL_EN = ['Extracell','Cytoplasm','Nucleus','Vacuole','Endoplasmic reticulum','Mitochondrion','Plasma membrane','Peroxisome','Chloroplast','Plastid','Cytoskeleton','Lysosome','Golgi apparatus', 'Centriole','Cell wall', 'Microsome']
EUK_OUTPUT_LABEL_TW = ['細胞外','細胞骨幹','細胞核','液泡','內質網','粒線體','質膜','過氧化體','葉綠體','色素體','細胞骨幹','溶酶體','高基氏體','中心粒','細胞壁','微粒體']
table = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y',]

def sendmail(subject,description,user_mail,file_name,user_id,project):  # Send Mail
    gmail_user = 'ms300kstudio@gmail.com'
    gmail_pwd = 'Rrrr1234'
    #這是GMAIL的SMTP伺服器，如果你有找到別的可以用的也可以換掉
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    #登入系統
    smtpserver.login(gmail_user, gmail_pwd)

    #寄件人資訊
    fromaddr = "*************@gmail.com"
    #收件人列表，格式為list即可
    toaddrs = user_mail
    msg = MIMEMultipart()
    msg["From"] = gmail_user
    msg["To"] = user_mail
    # --- Email 的主旨 Subject ---
    msg["Subject"] = subject
    part = MIMEText(description, _charset="UTF-8")
    msg.attach(part)
    #msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n" % (gmail_user, toaddrs, "Protein prediction"))
    ctype, encoding = mimetypes.guess_type('./predict/Upload/' + project + "/" + user_id+"/"+file_name+'.fasta')
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)

    fp = open('./predict/Upload/'+ project + "/" + user_id+"/"+file_name+'.fasta', "rb")
    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=file_name+".fasta")
    msg.attach(attachment)

    ctype, encoding = mimetypes.guess_type('./predict/Output/'+ project + "/" + user_id+"/"+file_name+'.txt')
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)

    fp = open('./predict/Output/'+ project + "/" + user_id+"/"+file_name+'.txt', "rb")
    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=file_name+".txt")
    msg.attach(attachment)
    smtpserver.sendmail(fromaddr, toaddrs, msg.as_string())
    smtpserver.quit()

def home(request):  # 首頁
    return render(request,"index.html")

def change_project(request):
    if request.POST['project']:
        request.session['project'] = request.POST['project']
        res = {
            "status":True
        }
        return JsonResponse(res ,safe=False)
    else:
        res = {
            "status":False
        }
        return JsonResponse(res ,safe=False)

def project(request): # 根據不同Project導致不同的功能頁面
    project = request.session['project']
    if not project:
        return HttpResponseRedirect('home')
    if 'user_id' not in request.session:
        request.session['user_id'] = str(random.randint(0,100000))
        path = "./predict/Output/" + project
        if not os.path.isdir(path):
            os.mkdir(path)
        path = "./predict/Output/" + project + "/" + request.session['user_id']
        if not os.path.isdir(path):
            os.mkdir(path)
        path = "./predict/Upload/" + project
        if not os.path.isdir(path):
            os.mkdir(path)
        path = "./predict/Upload/" + project + "/" + request.session['user_id']
        if not os.path.isdir(path):
            os.mkdir(path)
    else :
        path = "./predict/Output/" + project
        if not os.path.isdir(path):
            os.mkdir(path)
        path = "./predict/Output/" + project + "/" + request.session['user_id']
        if not os.path.isdir(path):
            os.mkdir(path)
        path = "./predict/Upload/" + project
        if not os.path.isdir(path):
            os.mkdir(path)
        path = "./predict/Upload/" + project + "/" + request.session['user_id']
        if not os.path.isdir(path):
            os.mkdir(path)

    return render(request, "project/" + project + "/project.html")


def goto_searchpost(request): #重新進入Project
    del request.session['visited']
    del request.session['email']
    del request.session['comment']
    return HttpResponseRedirect('project')


def download_file(request):  # 下載預測完檔案
    # do something
    project = request.session['project']
    file_name = request.GET['id']
    if project == "psldoc3" and request.GET['type'] == "Output":
        file_name = file_name.replace("fasta","txt")
    file_path='./predict/' + request.GET['type'] + '/' + project + "/" + request.GET['user_id']+"/" + file_name
    with open(file_path) as f:
        c = f.read()
    return HttpResponse(c)

def upload_file(request): # 下載預測所需要之檔案
    project = request.session['project']
    filename='./predict/Upload/' + project + "/" + request.GET['user_id']+"/"+request.GET['id']
    with open(filename) as f:
        c = f.read()
    return HttpResponse(c)

def history(request):
    project = request.session['project']

    if not project:
        return HttpResponseRedirect('home')

    if project:
        DATA_DIR = './predict/Upload/' + project + "/" + request.session['user_id']
        i = [];
        for filename in os.listdir(DATA_DIR):
            # print("Loading: %s" % filename)
            loadFile = open(os.path.join(DATA_DIR, filename), 'rb')
            filemt= time.localtime(os.stat(os.path.join(DATA_DIR, filename)).st_mtime)
            # print(time.strftime("%Y-%m-%d",filemt))
            # print(os.path.getsize(os.path.join(DATA_DIR, filename)),"bytes")
            i.append({
                "user_id":request.session['user_id'],
                "email":filename.split("-")[0],
                "filename":filename,
                "time":time.strftime("%Y-%m-%d",filemt),
                "size":os.path.getsize(os.path.join(DATA_DIR, filename))
            });
            loadFile.close()
        return render_to_response('history.html',locals())
    else:
        res = "No selected project"
        return JsonResponse(res ,safe=False)

def concate_array(target):
    total = np.array([])

    for i in range(0,len(target)):
        total = np.concatenate((total,target[i]), axis=0)
    m = hashlib.md5()
    m.update(total)
    answer = list(m.hexdigest())
    change_to_hex = []
    for i in answer:
        temp = int(i, 16)
        change_to_hex.append(temp)
    return change_to_hex

def tutorial(request):
    project = request.session['project']
    if not project:
        return HttpResponseRedirect('home')
    test_file = open('./Protein/templates/project/' + project +'/tutorial.pdf', 'rb')
    response = HttpResponse(content=test_file)
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % 'whatever'
    return response


def result(request):
    project = request.session['project']
    if not project:
        return HttpResponseRedirect('home')
    print("Now project: " + project)
    print("Comment: " + request.POST['comment'])
    print("Type: " + request.POST['type'])
    if project == "psldoc3" and request.POST['comment'] and request.POST['type']:
        request.session['email'] = request.POST['email']
        if not request.session['user_id']:
            request.session['user_id']=request.GET['id']
            filename = request.POST['email'] + "-" +request.GET['id']+".fasta"
            file_path="./predict/Upload/" + project + "/" + request.session['user_id']+"/"+filename
        else:
            filename = request.POST['email'] + "-" +request.GET['id']+".fasta"
            file_path="./predict/Upload/" + project + "/" + request.session['user_id']+"/"+filename
        with open(file_path, 'wb+') as destination:
            destination.write(request.POST['comment'])
        destination.close()
        sequence = ['']
        for i in request.POST['comment'].split('\r\n')[1:]:
            sequence[0] += i
        for i in sequence:
            x = pd.get_dummies(pd.Series(list(i)))
            x = x.T.reindex(table).T.fillna(0)
            A = x.values
            temp=[]
            final = concate_array(A)
        seq = final
        x_predict = array(seq)
        x_predict = x_predict.reshape(1,1,32)
        output_label_en = []
        output_label_tw = []
        if request.POST['type'] == 'prok':
            y_label = prok_one_hot_model.predict_classes(x_predict)[0]
            y_prob = prok_one_hot_model.predict_proba(x_predict)
            output_label_en = OUTPUT_LABEL_EN
            output_label_tw = OUTPUT_LABEL_TW
            data = [{},{},{},{},{},{},{},{},{}]

        else:
            y_label = euk_one_hot_model.predict_classes(x_predict)[0]
            y_prob = euk_one_hot_model.predict_proba(x_predict)
            output_label_en = EUK_OUTPUT_LABEL_EN
            output_label_tw = EUK_OUTPUT_LABEL_TW
            data = [{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}]
        temp = {}
        for i in range(0,len(output_label_en)):
            data[i]['tw'] = output_label_tw[i]
            data[i]['en'] = output_label_en[i]
            data[i]['prob'] = y_prob[0][i]
        filename = request.POST['email'] + "-" +request.GET['id']+".txt"
        file_path="./predict/Output/" + project + "/" + request.session['user_id']+"/"+filename
        with open(file_path, 'wb+') as destination:
            for i in range(0,len(output_label_en)):
                destination.write(output_label_en[i] + ": " + str(y_prob[0][i]) + '\n')
        destination.close()
        comment = request.POST['comment']
        label = output_label_tw[y_label] + " " + output_label_en[y_label]
        highest_score = y_prob[0][y_label]
        if request.POST['email']:
            filename = request.POST['email'] + "-" +request.GET['id']
            user_id = request.session['user_id']
            sendmail("Subcellular Localization Prediction","\n Send from NCCU Subcellular Localization prediction ",request.POST['email'],filename,user_id,project)
        filename = request.POST['email'] + "-" +request.GET['id']+".txt"
        return render_to_response('project/' + project + '/result.html',locals())
    else:
        print("Error: comment or email happened error!Or No selected project")
        res = "Error: comment or email happened error!Or No selected project"
        return JsonResponse(res ,safe=False)

#
# def load_file(request):
#     if 'visited' in request.session:
#         res=0
#         return JsonResponse(res,safe=False)
#     comment=request.session['comment']
#     if not comment :
#         filename = request.session['user_id']+".fasta"
#         file_path="./predict/Upload/"+request.session['user_id']+'/'+filename
#         path="./predict/"
#         os.chdir(path)
#         command="nextflow predict.nf --query Upload/"+request.session['user_id']+"/"+filename+" --output Output/"+request.session['user_id']+'/'+request.session['user_id']
#         os.system(command)
#     else:
#         print( "no in file")
#         filename=request.session['user_id']+".fasta"
#         path="./predict/"
#         os.chdir(path)
#         command="nextflow predict.nf --query "+"Upload/"+request.session['user_id']+"/"+filename+" --output Output/"+request.session['user_id']+"/"+request.session['user_id']
#         os.system(command)
#
#     p=Profile(user_name=request.session['user_id'],email=request.session['email'],comment=request.session['user_id'])
#     p.save()
#     filename="./predict/Output/"+request.session["user_id"]+"/"+request.session['user_id']+"/vote_score.txt"
#     with open(filename) as f:
#         c = f.read()
#     data=c
#     if type(request.session['email']) == str:
#         sendmail(request.session['email'],request.session['user_id'],request.session['user_id'],project)
#     request.session['visited']=True
#     res=0
#     reloads=0
#     return JsonResponse(res,safe=False)
