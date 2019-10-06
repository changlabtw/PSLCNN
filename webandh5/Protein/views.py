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
euk_one_hot_model = load_model('/Users/eric/new-protein-server/protein-server/euk_one_hot.h5')
prok_one_hot_model = load_model('/Users/eric/new-protein-server/protein-server/prok_one_hot.h5')
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

def run_shell_command(command_line):
    command_line_args = shlex.split(command_line)

    logging.info('Subprocess: "' + command_line + '"')

    try:
        command_line_process = subprocess.Popen(
            command_line_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        process_output, _ =  command_line_process.communicate()

        # process_output is now a string, not a file,
        # you may want to do:
        # process_output = StringIO(process_output)
        log_subprocess_output(process_output)
    except (OSError, CalledProcessError) as exception:
        logging.info('Exception occured: ' + str(exception))
        logging.info('Subprocess failed')
        return False
    else:
        # no exception was raised
        logging.info('Subprocess finished')

    return True
def sendmail(user_mail,file_name,user_id):

    info = ''
    info += ('\n'+"tes123"+'\n')
   # info += ('\n'+u'因資訊安全，請至(http://******.nchu-cm.com/)， 登入後觀看預警內容'+'\n')
    gmail_user = 'eric0330eric@gmail.com'
    gmail_pwd = 'rIcky42613'
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
    msg["Subject"] = "Subcellular Localization Prediction"
    part = MIMEText("\n Send from NCCU Subcellular Localization prediction ", _charset="UTF-8")
    msg.attach(part)
    #msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n" % (gmail_user, toaddrs, "Protein prediction"))
    ctype, encoding = mimetypes.guess_type('/Users/eric/new-protein-server/protein-server/predict/Upload/'+user_id+"/"+file_name+'.fasta')
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)

    fp = open('/Users/eric/new-protein-server/protein-server/predict/Upload/'+user_id+"/"+file_name+'.fasta', "rb")
    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=file_name+".fasta")
    msg.attach(attachment)

    ctype, encoding = mimetypes.guess_type('/Users/eric/new-protein-server/protein-server/predict/Output/'+user_id+"/"+file_name+'.txt')
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)

    fp = open('/Users/eric/new-protein-server/protein-server/predict/Output/'+user_id+"/"+file_name+'.txt', "rb")
    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=file_name+".txt")
    msg.attach(attachment)

    #smtpserver.sendmail(fromaddr, toaddrs, msg+info)
    #server = smtplib.SMTP('smtp.gmail.com', 587)
    #server.ehlo()
    #server.starttls()
    # --- 如果SMTP server 不需要登入則可把 server.login 用 # mark 掉
    #server.login(username,password)
    smtpserver.sendmail(fromaddr, toaddrs, msg.as_string())
    smtpserver.quit()
    #記得要登出
   # smtpserver.quit()
def is_fasta(filename):
    """with open (filename,'r') as handle:
        fasta = SeqIO.parse(handle,"fasta")
	print("fasta:")
	print(handle.read())
        return any(fasta)"""
    for record in SeqIO.parse(filename,"fasta",generic_dna):
        return any(record)
def home(request):
    return render(request,"index.html")

def search_post(request):

    # if 'visited' in request.session:
	# if request.session['visited']==True:
    #         url="result?id="+request.session['user_id']
    #         return HttpResponseRedirect(url)
    if 'user_id' not in request.session:
        request.session['user_id']=str(random.randint(0,100000))
        command="mkdir ./predict/Output/"+request.session['user_id']
        os.system(command)
        command="mkdir ./predict/Upload/"+request.session['user_id']
        os.system(command)
    else :
        path="./predict/Output/"+request.session['user_id']
        if not os.path.isdir(path):
            os.mkdir(path)
        path="./predict/Upload/"+request.session['user_id']
        if not os.path.isdir(path):
            os.mkdir(path)

    return render(request, "psldoc3.html")


def goto_searchpost(request):
    del request.session['visited']
    del request.session['email']
    del request.session['comment']
    return HttpResponseRedirect('psldoc3')
def download_file(request):
    # do something
    time.sleep(1)
    print(type(request.GET['id']))
    filename="/Users/eric/new-protein-server/protein-server/predict/Upload/"+request.session['user_id']+"/"+request.session['email']+'-'+request.GET['id']+'.fasta'
    with open(filename) as f:
        c = f.read()
    return HttpResponse(c)
def upload_file(request):
    print(type(request.GET['id']))
    filename="./predict/Upload/"+request.session['user_id']+"/"+request.GET['id']
    with open(filename) as f:
        c = f.read()
    return HttpResponse(c)
def history(request):
    DATA_DIR = './predict/Upload/'+request.session['user_id']
    i = [];
    for filename in os.listdir(DATA_DIR):
        print("Loading: %s" % filename)
        loadFile = open(os.path.join(DATA_DIR, filename), 'rb')
        filemt= time.localtime(os.stat(os.path.join(DATA_DIR, filename)).st_mtime)
        print(time.strftime("%Y-%m-%d",filemt))
        print(os.path.getsize(os.path.join(DATA_DIR, filename)),"bytes")
        i.append({
            "user_id":request.session['user_id'],
            "email":filename.split("-")[0],
            "filename":filename,
            "time":time.strftime("%Y-%m-%d",filemt),
            "size":os.path.getsize(os.path.join(DATA_DIR, filename))
        });
        loadFile.close()
    # if 'user_id' in request.session:
    #     i = Profile.objects.filter(user_name=request.session['user_id'])
    print(i)
    return render_to_response('new_history.html',locals())

import hashlib
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

table = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y',]

def result(request):
    if request.POST['comment'] and request.POST['type']:
        print(request.POST['comment'],request.POST['email'],request.POST['type'])
        request.session['email'] = request.POST['email']
        if not request.session['user_id']:
            request.session['user_id']=request.GET['id']
            filename = request.POST['email'] + "-" +request.GET['id']+".fasta"
            file_path="./predict/Upload/"+request.session['user_id']+"/"+filename
        else:
            filename = request.POST['email'] + "-" +request.GET['id']+".fasta"
            file_path="/Users/eric/new-protein-server/protein-server/predict/Upload/"+request.session['user_id']+"/"+filename
            print(file_path)
        with open(file_path, 'wb+') as destination:
            destination.write(request.POST['comment'])
        destination.close()
        sequence = ['']
        for i in request.POST['comment'].split('\r\n')[1:]:
            sequence[0] += i
        print(sequence)
        for i in sequence:
            x = pd.get_dummies(pd.Series(list(i)))
            x = x.T.reindex(table).T.fillna(0)
            A = x.values
            temp=[]
            final = concate_array(A)
        print(final)
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
            print(y_label,y_prob)

        else:
            y_label = euk_one_hot_model.predict_classes(x_predict)[0]
            y_prob = euk_one_hot_model.predict_proba(x_predict)
            output_label_en = EUK_OUTPUT_LABEL_EN
            output_label_tw = EUK_OUTPUT_LABEL_TW
            data = [{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}]
            print(y_label,y_prob)
        temp = {}
        print(output_label_en)
        for i in range(0,len(output_label_en)):
            data[i]['tw'] = output_label_tw[i]
            data[i]['en'] = output_label_en[i]
            data[i]['prob'] = y_prob[0][i]
        print(data)
        filename = request.POST['email'] + "-" +request.GET['id']+".txt"
        file_path="/Users/eric/new-protein-server/protein-server/predict/Output/"+request.session['user_id']+"/"+filename
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
            sendmail(request.POST['email'],filename,user_id)
        return render_to_response('localization_result.html',locals())
    else:
        print("Error: comment or email happened error!")

def old_result(request):
    data = []
    base_str = ""
    first_line = True
    if 'visited' in request.session:
        filename="./predict/Output/"+request.session['user_id']+"/"+request.GET['id']+"/vote_score.txt"
        with open(filename) as f:
            for line in f.readlines():
                if first_line is True:
                    first_line = False
                else:
                    data.append(line);
                    print(line)

        # data=c
        return render_to_response('new_result.html',locals())

    else:
        error=False
        comment=request.POST['comment']
        email = request.POST['email']
        request.session['email']=email
        request.session['comment']=comment
        if 'sessionid' in request.COOKIES:
            print("yes in session")
        #sid=request.COOKIES['sessionid']
        #print(sid)
        #sid = request.session.session_key
        #print(sid)

        request.session['user_id']=request.GET['id']
	#print("session: "+sid)
        #file_name="xxxx"
        testfile= request.POST.get('input_file',False)
        request.session['input_file']=testfile
        #@form = UploadFileForm(request.POST, request.FILES)
        #print request.POST
        #if form.is_valid():
        #    print "valid"
        #    handle_uploaded_file(request.FILES['input_file'])

        print ("comment: "+comment)
        print (testfile)
        files = [f for key, f in request.FILES.items()]
        print(files)
        if(( len(files)==0) and ( not comment )):
            error=True
            print ("both are None")
        else:
            if  not comment  :
                print("is file")
                filename = request.POST['email'] + "-" + request.GET['id']+".fasta"
                file_path="./predict/Upload/"+request.session['user_id']+"/"+filename
                handle_uploaded_file(files[0],file_path)
            else:
                print("is comment")
                filename = request.POST['email'] + "-" +request.GET['id']+".fasta"
                file_path="./predict/Upload/"+request.session['user_id']+"/"+filename
                with open(file_path, 'wb+') as destination:
                    destination.write(comment)
                destination.close()
            if is_fasta(file_path):
                error=False
                print("error = false")
            else:
                error=True
                print("error = true")

            #########################
            driver = webdriver.Chrome('/Users/eric/chromedriver')

            driver.get("https://www.ebi.ac.uk/QuickGO/slimming")

            change_block = driver.find_element_by_link_text("Input your own")
            change_block.click()
            input = driver.find_element_by_tag_name('textarea')

            print(input)
            driver.execute_script("$('textarea.default').click()")

            driver.execute_script("$('textarea.default').val('" + "GO:0008150,GO:0055085,GO:0006811,GO:0006520" + "')")
            count = 0
            for i in driver.find_elements_by_tag_name("textarea"):
                if count == 0:
                    i.send_keys(u'\ue00d')
                    count = count +1

            driver.execute_script("$('button.button').removeAttr('disabled');")
            count = 0
            for i in driver.find_elements_by_xpath("//*[contains(text(), 'Add terms to selection')]"):
                count = count + 1
                print(i)
                if count == 2:
                    i.click()

            # driver.find_element_by_link_text("Add terms to selection").click()
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            driver.find_element_by_class_name('chart-btn').click()
            time.sleep(3)
            base_str = driver.find_element_by_id('ancestorChart').get_attribute("ng-src")
            print(base_str)

            html = driver.page_source       # get html
            driver.get_screenshot_as_file("./sreenshot1.png")
            driver.close()

    #error = True
        if error==True:
            request.session['error']=error
            messages.warning(request,"Please correct the error below")
            return HttpResponseRedirect('psldoc3')
        reloads=1
        return render_to_response('new_result.html',locals())
# Create your views here.
def load_file(request):
    if 'visited' in request.session:
        res=0
        return JsonResponse(res,safe=False)
    comment=request.session['comment']
    if not comment :
        filename = request.session['user_id']+".fasta"
        file_path="./predict/Upload/"+request.session['user_id']+'/'+filename
        #handle_uploaded_file(files[0],file_path)
        path="./predict/"
        os.chdir(path)
        command="nextflow predict.nf --query Upload/"+request.session['user_id']+"/"+filename+" --output Output/"+request.session['user_id']+'/'+request.session['user_id']
        os.system(command)
    else:
        print( "no in file")
        filename=request.session['user_id']+".fasta"
        #fn=open(filename,"wb+")
        #fn.writelines(data)
        #fn.close()
        path="./predict/"
        os.chdir(path)
        command="nextflow predict.nf --query "+"Upload/"+request.session['user_id']+"/"+filename+" --output Output/"+request.session['user_id']+"/"+request.session['user_id']
        os.system(command)

    #file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    p=Profile(user_name=request.session['user_id'],email=request.session['email'],comment=request.session['user_id'])
    p.save()
        #data=request.POST['comment']
    filename="./predict/Output/"+request.session["user_id"]+"/"+request.session['user_id']+"/vote_score.txt"
    with open(filename) as f:
        c = f.read()
    data=c
    if type(request.session['email']) == str:
        sendmail(request.session['email'],request.session['user_id'],request.session['user_id'])
    request.session['visited']=True
    res=0
    reloads=0
    return JsonResponse(res,safe=False)
def handle_uploaded_file(f,f_path):
    with open(f_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
