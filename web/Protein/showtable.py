import sys
seq_list = {
    "A01234":0.89,
    "A05433":0.67,
    "A05233":0.22
}
def generate():
    color_list = [];
    for i in seq_list:
        temp_obj = {
            "label":i,
            "confidence":seq_list[i],
            "color":""
        }
        if seq_list[i] >= 0.9:
            temp_obj['color'] = "red"
        elif seq_list[i] >= 0.8:
            temp_obj['color'] = "orange"
        elif seq_list[i] >= 0.7:
            temp_obj['color'] = "yellow"
        elif seq_list[i] >= 0.6:
            temp_obj['color'] = "green"
        elif seq_list[i] >= 0.5:
            temp_obj['color'] = "blue"
        elif seq_list[i] >= 0.4:
            temp_obj['color'] = "blueviolet"
        elif seq_list[i] >= 0.3:
            temp_obj['color'] = "purple"
        elif seq_list[i] >= 0.2:
            temp_obj['color'] = "black"
        elif seq_list[i] >= 0.1:
            temp_obj['color'] = "black"
        else:
            temp_obj['color'] = "black"
        color_list.append(temp_obj)
    return color_list
if __name__ == '__main__':
    print(generate())
