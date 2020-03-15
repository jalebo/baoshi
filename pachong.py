# -*- coding:utf-8 -*-
import functools
from tkinter import *
# 导入ttk
from tkinter import ttk
from collections import OrderedDict
import binascii
KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]

class App(object):
    def __init__(self, mw):
        self.mw = mw
        self.initWidgets()
    def initWidgets(self):
        self.var = StringVar()    # 将label标签的内容设置为字符类型，用var来接收hit_me函数的传出内容用以显示在标签上
        self.l = Label(self.mw, text='请输入要转换的汉字：',  font=('Arial', 12), width=30, height=2)
        # 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
        self.l.pack()

        self.e1 = Entry(self.mw, show=None, font=('Arial', 14),textvariable=self.var)  # 显示成明文形式
        self.e1.pack()
        self.but = Button(self.mw,text=" 转  换 ",command=self.but1fun)
        self.but.pack()

        self.text = Text(self.mw, height=17, width=60,
        foreground='darkgray',
        font=('arial', 12)) 
        self.text.pack()
        st = ''
        self.text.insert(END, st)
        # 为text组件的右键单击事件绑定处理函数
        self.text.bind('<Button-3>', self.popup)
        # 创建Menu对象
        self.popup_menu = Menu(self.mw, tearoff = 0)
        self.my_items = (OrderedDict([('超大', 16), ('大',14), ('中',12),('小',10), ('超小',8)]),
        OrderedDict([('红色','red'), ('绿色','green'), ('蓝色', 'blue')]))
        for i,k in enumerate(['字体大小','颜色']):
            m = Menu(self.popup_menu, tearoff = 0)
            # 添加子菜单
            self.popup_menu.add_cascade(label=k ,menu = m)
            # 遍历OrderedDict的key（默认就是遍历key）
            for im in self.my_items[i]:
                m.add_command(label=im, command=functools.partial(self.choose, x=im))
        
        
    def but1fun(self):
        self.s = self.var.get()
        #print(self.s)
        self.li=self.printPlay(self.s , 1 , 0)
        #print(self.li)
        self.text.delete(1.0,END)
        for i in range(16):
            self.text.insert(END,int(self.li[i],2))
            self.text.insert(END,'\n')
        
    def popup(self, event):
        # 在指定位置显示菜单
        self.popup_menu.post(event.x_root,event.y_root)
    
    def choose(self, x):
        # 如果用户选择修改字体大小的子菜单项
        if x in self.my_items[0].keys():
        # 改变字体大小
            self.text['font'] = ('微软雅黑', self.my_items[0][x])
        # 如果用户选择修改颜色的子菜单项
        if x in self.my_items[1].keys():
        # 改变颜色
            self.text['foreground'] = self.my_items[1][x]

    def printPlay(self,textStr,line,background):
        # 初始化16*16的点阵位置，每个汉字需要16*16=256个点来表示，需要32个字节才能显示一个汉字
        # 之所以32字节：256个点每个点是0或1，那么总共就是2的256次方，一个字节是2的8次方
        rect_list = [] * 16
        for i in range(16):
            rect_list.append([] * 16)

        for text in textStr:
            #获取中文的gb2312编码，一个汉字是由2个字节编码组成
            gb2312 = text.encode('gb2312')
            #将二进制编码数据转化为十六进制数据
            hex_str = binascii.b2a_hex(gb2312)
            #将数据按unicode转化为字符串
            result = str(hex_str, encoding='utf-8')

            #前两位对应汉字的第一个字节：区码，每一区记录94个字符
            area = eval('0x' + result[:2]) - 0xA0
            #后两位对应汉字的第二个字节：位码，是汉字在其区的位置
            index = eval('0x' + result[2:]) - 0xA0
            #汉字在HZK16中的绝对偏移位置，最后乘32是因为字库中的每个汉字字模都需要32字节
            offset = (94 * (area-1) + (index-1)) * 32

            font_rect = None

            #读取HZK16汉字库文件
            with open("HZK16", "rb") as f:
                #找到目标汉字的偏移位置
                f.seek(offset)
                #从该字模数据中读取32字节数据
                font_rect = f.read(32)

            #font_rect的长度是32，此处相当于for k in range(16)
            for k in range(len(font_rect) // 2):
                #每行数据
                row_list = rect_list[k]
                for j in range(2):
                    for i in range(8):
                        asc = font_rect[k * 2 + j]
                        #此处&为Python中的按位与运算符
                        flag = asc & KEYS[i]
                        #数据规则获取字模中数据添加到16行每行中16个位置处每个位置
                        row_list.append(flag)               
        for row in range(16):
            for i in range(16):
                if rect_list[row][i]:
                    rect_list[row][i] = '1'
                else:
                    rect_list[row][i] = '0'
        for i in range(16):
            rect_list[i].reverse()
            rect_list[0][i] = ''.join(rect_list[i])   
        return(rect_list[0])
        #根据获取到的16*16点阵信息，打印到控制台
        #for row in rect_list:
           # for i in row:
                #if i:
                    #前景字符（即用来表示汉字笔画的输出字符）
                   # print(line, end='')
               # else:

                    # 背景字符（即用来表示背景的输出字符）
                   # print(background, end='')
            #print()


if __name__ == "__main__":
 mw = Tk()
 mw.title("汉字转16X16点阵")
 mw.geometry('360x400')
 App(mw)
 mw.mainloop()