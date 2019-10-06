
# coding: utf-8

# In[20]:


import tensorflow as tf
import keras
import numpy as np
import pandas as pd
from keras.utils import np_utils

X_train_seq = pd.read_csv('one_hot_seq_Prok.csv')


# In[21]:


print(X_train_seq)


# In[22]:


x_seq = []
for i in range(2585):
    x_seq.append(X_train_seq['Seq_Input'][i])


# In[23]:


print(x_seq[0])


# In[24]:


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


# In[25]:


"""One Hot Encoding for small_sample_sequence"""

table = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y',]

length = 2585

last_list = []
for i in range(0,length):

    """turn sequence input into one hot encoding"""

    x = pd.get_dummies(pd.Series(list(x_seq[i])))
    

    """make each sequence's encoding the same length because some may not have specific Alphabet ex:'Y' """
    x = x.T.reindex(table).T.fillna(0)

  
    """turn matrix into array"""
    
    A = x.values

    """concate 90*20 array into 1*1800 array"""
    temp=[]
#    print(type(A))
    final = concate_array(A)
    last_list.append(final)
    

print(last_list)

print(len(last_list))


# In[26]:


seq_file = open("Prok_label.txt","r")


# In[30]:


from collections import Counter

def Label(file):
    
    labels_dict=dict()
    detail_name = []
    counter = 0
    more_than_one_label = []
    numbers_of_label = []
    
    
    for lines in file.readlines():

        row = (lines.replace("\n","").split(";"))
        if len(row)>2:
            more_than_one_label.append(counter)
            numbers_of_label.append(len(row)-1)
        for x in row[:-1]:
            detail_name.append(x)
        counter+=1



    dict_for_more_than_one = dict(zip(more_than_one_label,numbers_of_label))



    keys = range(len(Counter(detail_name).keys()))
    names = Counter(detail_name).keys()



    counter = 0

    for name in names:
        labels_dict[name] = keys[counter]
        counter+=1

    label_list = []


    for label in detail_name:
        label_list.append(labels_dict[label])
        
    return label_list,dict_for_more_than_one,labels_dict


# In[31]:


label_file = open("Prok_label.txt","r")
labels,dict_extra,labels_dict = (Label(label_file))


print(labels_dict)


# In[32]:


print(last_list[0])


# In[33]:


from keras.utils import np_utils
length_seq = len(x_seq)
final_length = len(labels)
final_seq = []
for k in range(length_seq):
    if k in dict_extra.keys():
        for j in range(dict_extra[k]):
            final_seq.append(last_list[k])
    else:
        final_seq.append(last_list[k])


# In[34]:


print(len(final_seq[1]))


# In[35]:


print(len(final_seq[44]))
print(len(final_seq[77]))
print(final_seq[0])


# In[36]:


"""One Hot Encoding for small_sample_label"""

small_sample_label_OneHot = np_utils.to_categorical(labels)

print((small_sample_label_OneHot.shape))
print(small_sample_label_OneHot)


# In[37]:


final_seq = np.asarray(final_seq)
final_seq = final_seq.reshape(2799,1,32)
print(final_seq.shape)


# In[38]:


from keras.layers import Dense,Dropout,Flatten,Conv2D,AveragePooling2D,MaxPooling2D,Conv3D,AveragePooling3D,LSTM,GRU,Activation,Conv1D,MaxPooling1D
from keras.models import Sequential,load_model
from keras.layers.wrappers import TimeDistributed
from keras import optimizers
high_acc = 0
max_filter = 0

model = Sequential()
model.add(Conv1D(filters=64, kernel_size=3, strides=1, padding='same',input_shape=(1,32),activation='relu'))
model.add(MaxPooling1D(pool_size=1, strides=3, padding='valid'))
model.add(Conv1D(filters=64, kernel_size=3, strides=1, padding='same',input_shape=(1,32),activation='relu'))
model.add(MaxPooling1D(pool_size=1, strides=3, padding='valid'))
model.add(Flatten())
model.add(Dropout(0.25))
model.add(Dense(5000,activation='relu'))
model.add(Dropout(0.25))
model.add(Dense(9,activation='softmax'))
model.summary()



# In[39]:


print(type(final_seq))


# In[40]:


model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer='adam',
              metrics=['accuracy'])


train_history = model.fit(x=final_seq,y=small_sample_label_OneHot,validation_split=0.2,epochs=100,batch_size=200,verbose=2)



# In[87]:


scores = model.evaluate(final_seq,small_sample_label_OneHot)
'''accuracy'''
print('accuracy',scores[1])
'''loss'''
print('lost',scores[0])


# In[41]:


model.save('prok_one_hot.h5')


# In[42]:


"""for all the predictions"""
from keras.models import load_model
y_predict_label = []
y_predict_prob = []
one_hot_model = load_model('prok_one_hot.h5')
for seq in final_seq:
    
    x_predict = seq.reshape(1,1,32)
    y_label = one_hot_model.predict_classes(x_predict)[0]
    y_prob = one_hot_model.predict_proba(x_predict)
    tmp = []
    
    for k in range(len(y_prob[0])):
        tmp.append(float(y_prob[0][k]))
    
    y_predict_label.append(y_label)
    y_predict_prob.append(tmp)


# In[43]:


print(y_predict_prob)


# In[44]:


predict_names = []

for label in y_predict_label:
    for key in labels_dict.keys():
        if label == labels_dict[key]:
            predict_names.append(key)
            
print(predict_names)


# In[108]:


print(y_predict_prob[0])


# In[109]:


print(y_predict_prob[1])

