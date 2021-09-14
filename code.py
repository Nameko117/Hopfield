# -*- coding: utf-8 -*-


import tkinter as tk
from tkinter import ttk

FILENAME = ['Basic_Training', 'Basic_Testing', 'Bonus_Training', 'Bonus_Testing', 'Basic_Testing_plus']

# 讀入資料
def read_file(file_name):
    xs = []
    x = []
    f = open(file_name + ".txt")
    for line in f:
        if line == '\n':
            xs.append(x)
            x = []
            continue
        line = line.replace("\n", "")
        for i in range(len(line)):
            if line[i] == ' ':
                x.append(-1)
            elif line[i] == '1':
                x.append(1)
    xs.append(x)
    f.close()
    return xs

# 訓練
def train(xs):
    # get weight
    w = []
    for i in range(len(xs[0])):
        tw = []
        for j in range(len(xs[0])):
            tw.append(0)
        w.append(tw)
    # 1/p * sigma(xk * xkT)
    for k in range(len(xs)):
        x = xs[k]
        for i in range(len(x)):
            for j in range(len(x)):
                w[i][j] += (x[i] * x[j]) / len(xs[0])
    # -N/p I
    for i in range(len(xs[0])):
        w[i][i] = 0
    # get sita
    sita = []
    for i in range(len(xs[0])):
        sita.append(0)
        '''
        for j in range(len(xs[0])):
            sita[i] += w[i][j]
            '''
    return [w, sita]

# 測試
def test(xs, w, sita):
    for k in range(len(xs)):
        x = xs[k]
        n = 0
        same = 0
        while n < 10000:
            i = n%len(x)
            if same == len(x):
                break
            # sigma(wj * x)
            t = 0
            for j in range(len(x)):
                t += w[i][j] * x[j]
            t -= sita[i]
            # sgn(uj - sitaj)
            if t > sita[i]:
                tx = 1
            elif t == sita[i]:
                tx = x[i]
            elif t < sita[i]:
                tx = -1
            # x(n+1)
            if x[i] == tx:
                same += 1
            else:
                same = 0
                x[i] = tx
            n += 1
        xs[k] = x
    return xs

# 可視化
def getImg(x, n):
    t = ""
    for i in range(len(x)):
        if x[i] == -1:
            t += '○'
        elif x[i] == 1:
            t += '●'
        if i%n == n-1:
            t += '\n'
    return t

def start():
    global file, train_page, test_page
    file = data_combo.get()
    train_page = 0
    test_page = 0
    show()
    

def show():
    global train_page, test_page, train_label, test_label
    if file == 'Basic':
        train_page %= len(basic_train)
        test_page %= len(basic_test)
        train_data.configure(text=getImg(basic_train[train_page], 9))
        test_in_data.configure(text=getImg(basic_test[test_page], 9))
        test_out_data.configure(text=getImg(basic_y[test_page], 9))
        rate_label.configure(text="回想成功率：" + str(basic_rate))
    elif file == 'Basic_plus':
        train_page %= len(basic_train)
        test_page %= len(basic_test_plus)
        train_data.configure(text=getImg(basic_train[train_page], 9))
        test_in_data.configure(text=getImg(basic_test_plus[test_page], 9))
        test_out_data.configure(text=getImg(basic_plus_y[test_page], 9))
        rate_label.configure(text="回想成功率：" + str(basic_plus_rate))
    elif file == 'Bonus':
        train_page %= len(bonus_train)
        test_page %= len(bonus_test)
        train_data.configure(text=getImg(bonus_train[train_page], 10))
        test_in_data.configure(text=getImg(bonus_test[test_page], 10))
        test_out_data.configure(text=getImg(bonus_y[test_page], 10))
        rate_label.configure(text="回想成功率：" + str(bonus_rate))
    train_label.configure(text='訓練資料'+str(train_page+1))
    test_label.configure(text='測試輸入／輸出'+str(test_page+1))
        
def next():
    global train_page, test_page
    train_page += 1
    test_page += 1
    show()
    
def getRate(xs, ys):
    correct = 0
    for i in range(len(xs)):
        if xs[i] == ys[i]:
            correct += 1
    return correct/len(xs)


# train & test
basic_train = read_file(FILENAME[0])
basic_test = read_file(FILENAME[1])
basic_test_plus = read_file(FILENAME[4])
bonus_train = read_file(FILENAME[2])
bonus_test = read_file(FILENAME[3])

[basic_w, basic_sita] = train(basic_train)
[bonus_w, bonus_sita] = train(bonus_train)

basic_y = test(read_file(FILENAME[1]), basic_w, basic_sita)
basic_plus_y = test(read_file(FILENAME[4]), basic_w, basic_sita)
bonus_y = test(read_file(FILENAME[3]), bonus_w, bonus_sita)

basic_rate = getRate(basic_train, basic_y)
basic_plus_rate = getRate(basic_train, basic_plus_y)
bonus_rate = getRate(bonus_train, bonus_y)

file = ''
train_page = 0
test_page = 0

# 開新視窗
window = tk.Tk()
# 設計視窗
window.title('107502508')
window.geometry('400x600')
window.configure(background='white')
# 標題
header_label = tk.Label(window, text='Hopfield類神經網路')
header_label.pack()

# basic or bonus
data_frame = tk.Frame(window)
data_frame.pack(side=tk.TOP)
data_combo = ttk.Combobox(data_frame, values=['Basic', 'Basic_plus', 'Bonus'], state="readonly")
data_combo.current(0)
data_combo.pack(side=tk.TOP)
data_btn = tk.Button(window, text='訓練', command=start)
data_btn.pack(side=tk.TOP)
rate_label = tk.Label(window)
rate_label.pack(side=tk.TOP)
train_btn = tk.Button(window, text='下一個', command=next)
train_btn.pack(side=tk.TOP)

# train data
train_frame = tk.Frame(window)
train_frame.pack(side=tk.TOP)
train_label = tk.Label(train_frame, text='訓練資料')
train_label.pack(side=tk.LEFT)
train_data = tk.Label(window, text='')
train_data.pack(side=tk.TOP)

# test data
test_frame = tk.Frame(window)
test_frame.pack(side=tk.TOP)
test_label = tk.Label(test_frame, text='測試輸入／輸出')
test_label.pack(side=tk.LEFT)
test_data_frame = tk.Frame(window)
test_data_frame.pack(side=tk.TOP)
test_in_data = tk.Label(test_data_frame, text='')
test_in_data.pack(side=tk.LEFT)
test_out_data = tk.Label(test_data_frame, text='')
test_out_data.pack(side=tk.LEFT)

# 執行視窗
window.mainloop()

