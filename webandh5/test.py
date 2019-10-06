from keras.models import load_model
from numpy import array
y_predict_label = []
y_predict_prob = []
one_hot_model = load_model('prok_one_hot.h5')

seq = [6,3,4,1,1,9,12,0,6,12,7,7,1,10,9,6,3,7,2,7,1,14,2,15,12,7,5,6,7,4,3,9]
x_predict = array(seq)
x_predict = x_predict.reshape(1,1,32)
y_label = one_hot_model.predict_classes(x_predict)[0]
y_prob = one_hot_model.predict_proba(x_predict)

print(y_label,y_prob)
