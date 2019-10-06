file_name ='Localization/SP-Prok.txt'
f = open(file_name,'r')

count = 0;
seq_id = "";
seq_content = "";

label = []
for i in f.readlines():  
    # print(i.replace('\n',''))
    if count % 3 == 0:
        seq_id = i
    elif count % 3 == 1:
        seq_content = i
    if count % 3 == 2:
        label.append(i)
        # w = open('SP-Prok/'+str(count/3)+'_'+seq_id.replace('\n','')+'.fasta','w+')
        # w.write(seq_id)
        # w.write(seq_content)
        # w.close()
    count += 1

w = open('Prok_label.txt','w+')
for i in label:
    w.write(i)

w.close()
