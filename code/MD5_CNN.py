# coding: utf-8

"""  Variable Defination Start """

SEQ_SPLIT_LEN = 90
AMINO_LEN = 20


"""  Variable Defination Over """


# smp 切割所需 pssm 陣列
import glob
def SMP2LIST(SMPFILE,open):
    file_name = SMPFILE
    f = open(file_name,'r')
    final = []
    counter = 0
    for i in f.readlines():
        if counter>=4 and counter<=93:
            final.append(i.split()[2:22])
            if counter == 93:    #長度超過93drop掉
                break
        counter+=1
    return final



#Change to Exponetial Number
from math import exp
def NUM2EXP(num):
    answer = 1/(1+exp((float(num))*(-1)))
    return answer


Rat_matrix= []
label_name = []

for filename in glob.glob('smp/*.smp'):

    Temp = SMP2LIST(filename,open)
    if len(Temp) < SEQ_SPLIT_LEN:    #少於長度90過濾掉
        #filter_list.append(filename)
        continue
    else:
        label_name.append(filename)
        Rat_matrix.append(Temp)


# 將Lable由name轉為數字

label_list = []
for i in range(len(Rat_matrix)):
    if 'GO:122' in label_name[i]:
        label_list.append(0)
    elif 'GO:7186' in label_name[i]:
        label_list.append(1)
    elif 'GO:45944' in label_name[i]:
        label_list.append(2)
    elif 'GO:50911' in label_name[i]:
        label_list.append(3)





#檢查有錯誤的pssm


del_list = []
for i in range(0,len(Rat_matrix)):
    for j in range(0,SEQ_SPLIT_LEN):
        if len(Rat_matrix[i][j]) != AMINO_LEN:
            if i not in del_list:
                del_list.append(i)
                print(len(Rat_matrix[i][j]),i,j)



#刪除有錯誤的pssm

offset = 0
for i in del_list:
    print(i)
    del Rat_matrix[i+offset]
    del label_list[i+offset]
    offset -= 1

print("len ",len(Rat_matrix))
print("len ",len(label_list))



import tensorflow as tf
import keras
import numpy as np
import pandas as pd
from keras.utils import np_utils
PSSM_SEQ = np.zeros((len(Rat_matrix),SEQ_SPLIT_LEN,AMINO_LEN))


for i in range(0,len(Rat_matrix)):
    for j in range(0,SEQ_SPLIT_LEN):
        for k in range(0,AMINO_LEN):
            #正常情況
            if (len(str(Rat_matrix[i][j][k]).split('-')) == 2 and str(Rat_matrix[i][j][k]).split('-')[0] == '') or len(str(Rat_matrix[i][j][k]).split('-')) == 1:
                PSSM_SEQ[i][j][k] = Rat_matrix[i][j][k]
            #異常情況 -6-10 or -3-4
            else:
                PSSM_SEQ[i][j][k] = float('-' + str(Rat_matrix[i][j][k]).split('-')[1])
                print("error pssm ",i,j,k)



PSSM_LABEL = np_utils.to_categorical(label_list)
PSSM_LABEL = PSSM_LABEL.reshape((len(Rat_matrix),4))

"""   Data Preprocessing Over  """


"""  CNN Model for small_sample_label  """
from keras.layers import Dense,Dropout,Flatten,Conv2D,AveragePooling2D,MaxPooling2D,Conv3D,AveragePooling3D,LSTM,GRU,Activation,Conv1D,MaxPooling1D
from keras.models import Sequential
from keras.layers.wrappers import TimeDistributed
from keras import optimizers
from keras.optimizers import RMSprop
high_acc = 0
max_filter = 0
for i in range(2,5):
    model = Sequential()

    model.add(Conv1D(filters=64, kernel_size=SEQ_SPLIT_LEN, strides=1, padding='same',input_shape=(SEQ_SPLIT_LEN,AMINO_LEN),activation='relu'))
    model.add(MaxPooling1D(pool_size=64, strides=32, padding='valid'))
    model.add(Flatten())
    model.add(Dropout(0.25))
    model.add(Dense(5000,activation='relu'))
    model.add(Dropout(0.25))
    model.add(Dense(4,activation='softmax'))

    model.summary()
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer='adam',
                  metrics=['accuracy'])
    train_history = model.fit(x=PSSM_SEQ,y=PSSM_LABEL,validation_split=0.2,epochs=30,batch_size=200,verbose=2)
    scores = model.evaluate(PSSM_SEQ,PSSM_LABEL)

    '''accuracy'''
    print('accuracy',scores[1])
    if scores[1] > high_acc:
        high_acc = scores[1]
        max_filter = i
    '''loss'''
    print('lost',scores[0])
