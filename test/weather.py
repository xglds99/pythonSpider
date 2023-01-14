from tkinter import *   #init all=[方法]
from tkinter import messagebox
import urllib.request
import requests
#根据用户输入的城市查询天气
def weather():
    #获取用户输入的城市
    city = entry.get()
    # print(city)
    if city == '':
        messagebox.showinfo('提示','请输入要查询的城市')
    else:

        #url编码
        city = urllib.request.quote(city)
        host = 'https://jisutqybmf.market.alicloudapi.com/weather/query'

        appcode = 'c91adb3532c84e8993ee22e3013b363f'
        querys = 'city='+city
        header = {'Authorization': 'APPCODE ' + appcode}
        url = host + '?' + querys

        request = requests.get(url,header = header).json()
        info = request['result']
        lis.delete(0,END)
        lis.insert(0,"星期：%s"%info['week'])
        lis.insert(1, "天气：%s" % info['weather'])
        lis.insert(2, "温度：%s" % info['temp'])
        lis.insert(3, "风向：%s" % info['winddirect'])




#创建窗口
root = Tk()
#标题
root.title('天气查询')
#窗口大小
root.geometry('500x400')
#窗口出现的位置令他出现在桌面中央
root.geometry('+500+300')
#标签控件
label = Label(root,text='输入要查询的城市名字：')
#定位  grid 网格式布局  pack  place
label.grid()
#输入控件
entry = Entry(root,font = ('微软雅黑',22))
#重新定位  网格
entry.grid(row=0,column=1)
#列表框控件
lis = Listbox(root,font=('微软雅黑',15),width=40,height=10)
#定位  跨列合并
lis.grid(row = 1,columnspan = 2 )
#按钮 sticky为对其分W\E\N\S
button = Button(root,text='查询',width=10,command = weather)
button.grid(row=2,column=0,sticky=W)
#root.quit退出页面 commend点击触发的方法
button1 = Button(root,text='退出',width=10,command=root.quit)
button1.grid(row=2,column=1,sticky=E)

#显示窗口  消息循环
root.mainloop()