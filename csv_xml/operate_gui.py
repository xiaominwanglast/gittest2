#coding:utf-8
from Tkinter import *
import tkFileDialog
from operate import operate
import ConfigParser
import os
from write_ele_csv import xml_csv
class xml_gui(object):
    #文本类型
    options={}
    options['defaultextension'] = '.txt'
    options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
    def __init__(self):
        #初始化TK窗口
        self.root=Tk()
        self.root.title('excel_changeto_xml')
        self.root.geometry("400x300")
        self.default_path=os.path.abspath(os.getcwd())+'\\config.ini'
    def main(self):
        def xmlcallback():
            test = operate()
            test.xlsx_to_dic()
            test.dic_to_xml()
        def csvcallback():
            cf = ConfigParser.ConfigParser()
            with open(self.default_path) as cfconfig:
                cf.readfp(cfconfig)
            filename_csv = cf.get('data', 'test_path')
            xml_csv().read_xml_to_csv(filename_csv)
        def selectPath():
            path_ = tkFileDialog.askopenfilename(filetypes=self.options['filetypes'])
            #将获取的path_路径传入到condfig内
            cf = ConfigParser.ConfigParser()
            with open(self.default_path,'rb') as fsconfig:
                cf.readfp(fsconfig)
            cf.set('data','test_path',path_)
            cf.write(open(self.default_path,'w'))
            path.set(path_)
        path = StringVar()
        Label(self.root, text=u"目标路径:").grid(row=0, column=0)
        Entry(self.root, textvariable=path).grid(row=0, column=1)
        Button(self.root, text=u"路径选择", command=selectPath).grid(row=0, column=2)
        Button(self.root, text=u'将excel文件转为xml文件', command=xmlcallback).grid(row=2, column=0)
        Button(self.root,text='quit',command=self.root.destroy).grid(row=4,column=2)
        Button(self.root,text=u'将xml文件转成excel文件',command=csvcallback).grid(row=3,column=0)
        self.root.mainloop()

if __name__=='__main__':
    xml_gui().main()