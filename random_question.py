from tkinter import *
from tkinter import messagebox
import os
import threading
import random

app = Tk()
app.geometry("400x200")

tip = Label(app, text="请记录问题")
tip.place(x=5,y=0)
entry = Entry(app, width=20)
entry.place(x=5,y=20)

tip1Val = StringVar()
tip1 = Label(app, textvariable=tip1Val)
tip1.place(x=5,y=50)

currQuestionVal = StringVar()
tip2 = Message(app, textvariable=currQuestionVal, width=200)
tip2.place(x=50,y=80)

tmp_file = 'q-list.txt'
time_speed = 2*60*60 # 2小时
timer = None

# 判断是否存在问题缓存文件
def isFileExit():
    return os.path.exists(tmp_file)
# 获取缓存文件内的行数
def getFileRowLen():
    return len(open(tmp_file, encoding='gbk').readlines())
# 展示当前问题
def showCurrQuestion(q):
    if q == None:
        currQuestionVal.set("当前问题：无")
    else:
        currQuestionVal.set("当前问题：{}".format(q))
# 定时提醒
def timeView():
    question = getQuestionByRandom()
    global timer
    if question != None:
        m = messagebox.showinfo(title="question", message=question)
        timer = threading.Timer(time_speed, timeView)
        timer.start()
# 随机获取一个问题并进行展示并返回问题
def getQuestionByRandom():
    if isFileExit():
        q_list = open(tmp_file, encoding='gbk').readlines()
        randomQuestion = q_list[random.randint(0,getFileRowLen() - 1)]
        showCurrQuestion(randomQuestion)
        return randomQuestion
    else:
        return None
# 展示最新条数
def checkListLen():
    if isFileExit():
        l = getFileRowLen()
        tip1Val.set("已存在{}个问题".format(str(l)))
    else:
        tip1Val.set("已存在0个问题")
def getInp():
    inp = entry.get()
    if inp == '':
        messagebox.showerror(title="question", message='未输入')
        return
    if isFileExit():
        # 追加内容
        f = open('q-list.txt', 'a', encoding='gbk')
        oldLen = getFileRowLen()
        f.write("{}. {}".format(str(oldLen+1),inp))
        f.write('\n')
        f.close()
    else:
        f = open('q-list.txt', 'w', encoding='gbk')
        f.write("1. {}".format(inp))
        f.write('\n')
        f.close()
    entry.delete(0, END)
    checkListLen()
# 开始/停止
def startOrPause():
    if btn['text'] == '开始':
        btn['text'] = '停止'
        timeView()
    else:
        btn['text'] = '开始'
        if timer != None:
            timer.cancel()
button = Button(app, text="提交", command=getInp)
button.place(x=300,y=20)
btn = Button(app, text="开始", command=startOrPause)
btn.place(x=350,y=20)

showCurrQuestion(None)
checkListLen()

def closeWin():
    #try:
    if timer != None:
        timer.cancel()
    app.destroy()
    #except NameError:
        #app.destroy()
app.protocol("WM_DELETE_WINDOW", closeWin)

app.mainloop()
