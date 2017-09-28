#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('gbk')

import csv
import xlwt
from xml.etree.ElementTree import iterparse
from HTMLParser import HTMLParser
import os
class xml_csv(object):
    def __init__(self):
        #初始化生成文件表格.
        self.keywords={"testsuit_name":u'项目名','testcase_name':u'用例名',"version":u'版本',
                       "summary":u'描述',"preconditions":u'前提', "importance":u"重要性",'step_number':u'步骤序号','actions':u'动作描述','expectedresults':u'期望结果', "keywords":u'关键词'}
        self.default_path=os.path.abspath(os.getcwd())
        self.suite_list=self.create_list(10)
        self.case_list=self.create_list(10)
    def __str__(self):
        """
        :return: self.keywords
        """
        return ''.join(self.keywords.values())

    @classmethod
    def dill_data(cls,data):
        """
        :param data: 需要处理数据
        :return: 返回处理后的数据
        """
        return data.replace('![','').replace('<p>','').replace('</p>','').replace(']]','').replace('CDATA[','')

    @classmethod
    #返回空数组
    def create_list(cls,count):
        data=[]
        for eve_data in range(count):
            data.append('')
        return data

    # 去掉xml文件中的HTML标签
    # 使用htmlparser 去除text文本多余修饰
    def strip_tags(self, htmlStr):
        htmlStr = htmlStr.strip()
        htmlStr = htmlStr.strip("\n")
        result = []
        parser = HTMLParser()
        parser.handle_data = result.append
        parser.feed(htmlStr)
        parser.close()
        return ''.join(result)
    """
    def write_xml_csv(self):
        with open(self.work_path,'rb') as work_fs:
            work_data=work_fs.read()
        testsuite=self.get_values(r'<testsuite name="(.*?)">',work_data)
        testcases=self.get_values(r'<testcase.*?</testcase>',work_data)
        for testcase in testcases:
            print testcase
            list_data_line=[]
            testcase_name=self.get_values(r'<testcase name="(.*?)">',testcase)
            version=self.get_values(r'<version><(.*?)]></version>',testcase)
            summary=self.get_values(r'<summary><(.*?)></summary>',testcase)
            preconditions=self.get_values('<preconditions><(.*?)></preconditions>',testcase)
            importance=self.get_values('<importance><(.*?)></importance>',testcase)
            steps=self.get_values('<step>(.*?)</step>',testcase)
            for step in steps:
                print step
                step_number=self.get_values('<step_number><(.*?)></step_number>',step)
                actions=self.get_values('<actions><(.*?)></actions>',step)
                expectedresult=self.get_values('<expectedresults><(.*?)></expectedresults>',step)
    """
    def read_xml_to_csv(self,xmlfile):
        csv_file=xmlfile.split('.')[0]+'.csv'
        csvfile = open(csv_file, 'wb')
        spamwriter = csv.writer(csvfile, dialect='excel')
        spamwriter.writerow([self.keywords['testsuit_name'],self.keywords['testcase_name'],self.keywords['version'],self.keywords['summary'],self.keywords['preconditions'],
                             self.keywords['importance'],self.keywords['step_number'],self.keywords['actions'],self.keywords['expectedresults'],self.keywords['keywords']])

        # 解析xml，分为两块，一块为testsuit，一块为testcase
        for (event, node) in iterparse(xmlfile, events=['start']):
            #element.tag为节点
            #element.text为节点内容
            if node.tag == "testsuite":
                self.suite_list[0] = node.attrib['name']
                '''
                for child in node:
                    if child.tag == "node_order":
                        print child.text
                        suite_list[2] = child.text
                '''
                spamwriter.writerow(self.suite_list)
            if node.tag == "testcase":
                self.case_list[1]=node.attrib['name']
              #  print node.attrib['internalid']
              # case_list[4] = node.attrib['internalid']
                for child in node:
                    if child.tag == "version":
                        self.case_list[2] = child.text
                    if child.tag == "summary":
                        self.case_list[3] = self.strip_tags(str(child.text))
                    if child.tag == "preconditions":
                        self.case_list[4] = self.strip_tags(str(child.text))
                    if child.tag == "importance":
                        self.case_list[5] = self.strip_tags(str(child.text))
                    if child.tag == "keywords":
                        self.case_list[9] = self.strip_tags(str(child.text))
                    if child.tag == "steps":
                        for children in child:
                            if children.tag=="step":
                                for gpchild in children:
                                    if gpchild.tag== "step_number":
                                        self.case_list[6]=self.strip_tags(str(gpchild.text))
                                    if gpchild.tag == "actions":
                                        self.case_list[7]=self.strip_tags(str(gpchild.text))
                                    if gpchild.tag == "expectedresults":
                                        self.case_list[8]=self.strip_tags(str(gpchild.text))
                                spamwriter.writerow(self.case_list)
                                self.case_list = self.create_list(10)
        csvfile.close()

    #封装类方法
    #将csv文件写成
    @classmethod
    def csv_xls(cls,path):
        myexcel = xlwt.Workbook()
        mysheet = myexcel.add_sheet("Sheet1")
        csvfile = file(path, "rb")
        reader = csv.reader(csvfile)
        l = 0
        for line in reader:
            r = 0
            for i in line:
                mysheet.write(l, r, i)
                r = r + 1
            l = l + 1
        myexcel.save(path)
if __name__=='__main__':
    xml_csv().read_xml_to_csv('test.xml')