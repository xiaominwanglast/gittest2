#coding:utf-8
from easy_excel import easy_excel
import os
import ConfigParser
class operate(object):
    work_path = os.path.abspath(os.getcwd()) + '\\config.ini'
    def __init__(self):
        self.path=self.readcf
        self.temp = easy_excel(self.path)
        self.dic_testlink = {}
        self.row_flag = 2
        #testsuite 获取值为name
        self.testsuite = self.temp.getCell('Sheet1', 1, 1)
        self.dic_testlink[self.testsuite] = {"node_order": "", "details": u"测试部测试用例", "testcase": []}
        self.content = ""
        self.content_list = []

    @property
    def readcf(self):
        cf = ConfigParser.ConfigParser()
        print self.work_path
        with open(self.work_path) as cfconfig:
            cf.readfp(cfconfig)
        filename_csv = cf.get('data', 'test_path')
        return filename_csv

    def xlsx_to_dic(self):
        while True:
            # print 'loop1'
            # list_testcase = dic_testlink[testsuite].["testcase"]
            #name为testcase的name，node_order默认值
            #version版本号，summary 摘要，preconditions 前提，importance 重要性（3个阶层1,2,3），steps步骤（step_number,actions,expectedresults),关键词是 keywords
            testcase = {"name": "", "node_order": "100", "externalid": "", "version": "1.0.0", "summary": "","preconditions": "", "execution_type": "1", "importance": "3", "steps": [], "keywords": "P1"}
            #testcase的name
            testcase["name"] = self.temp.getCell('Sheet1', self.row_flag, 1)
            testcase["summary"] = self.temp.getCell('Sheet1', self.row_flag, 3)
            testcase["preconditions"] = self.temp.getCell('Sheet1', self.row_flag, 6)
            step_number = 1
            #关键词
            testcase["keywords"] = self.temp.getCell('Sheet1', self.row_flag, 2)
            print testcase["keywords"]
            while True:
                # "execution_type" 执行类型
                step = {"step_number": "", "actions": "", "expectedresults": "", "execution_type": ""}
                step["step_number"] = step_number
                step["actions"] = self.temp.getCell('Sheet1', self.row_flag, 7)
                step["expectedresults"] = self.temp.getCell('Sheet1', self.row_flag, 8)
                testcase["steps"].append(step)
                step_number += 1
                self.row_flag += 1
                if self.temp.getCell('Sheet1', self.row_flag, 1) is not None or self.temp.getCell('Sheet1',self.row_flag,7) is None:
                    break
            self.dic_testlink[self.testsuite]["testcase"].append(testcase)
            # print self.row_flag
            if self.temp.getCell('Sheet1', self.row_flag, 5) is None and self.temp.getCell('Sheet1', self.row_flag + 1,5) is None:
                break
        self.temp.close()
        # print self.dic_testlink

    def content_to_xml(self, key, value=''):
        if key == 'step_number' or key == 'execution_type' or key == 'node_order' or key == 'externalid' or key == 'version' or key == 'importance' or key=='details':
            return "<" + str(key) + "><![CDATA[" + str(value) + "]]></" + str(key) + ">"
        elif key == 'actions' or key == 'expectedresults' or key == 'summary' or key == 'preconditions':
            return "<" + str(key) + "><![CDATA[<p> " + value + "</p> ]]></" + str(key) + ">"
        elif key == 'keywords':
            return '<keywords><keyword name="' + value + u'"><notes><![CDATA[ 每个版本都会执行的用例]]></notes></keyword></keywords>'
        elif key == 'name':
            return '<testcase name="' + value + '">'
        else:
            return '##########'

    def dic_to_xml(self):
        testcase_list = self.dic_testlink[self.testsuite]["testcase"]
        for testcase in testcase_list:
            for step in testcase["steps"]:
                self.content += "<step>"
                self.content += self.content_to_xml("step_number", step["step_number"])
                self.content += self.content_to_xml("actions", step["actions"])
                self.content += self.content_to_xml("expectedresults", step["expectedresults"])
                self.content += self.content_to_xml("execution_type", step["execution_type"])
                self.content += "</step>"
            self.content = "<steps>" + self.content + "</steps>"
            self.content = self.content_to_xml("importance", testcase["importance"]) + self.content
            self.content = self.content_to_xml("execution_type", testcase["execution_type"]) + self.content
            self.content = self.content_to_xml("preconditions", testcase["preconditions"]) + self.content
            self.content = self.content_to_xml("summary", testcase["summary"]) + self.content
            self.content = self.content_to_xml("version", testcase["version"]) + self.content
            self.content = self.content_to_xml("externalid", testcase["externalid"]) + self.content
            self.content = self.content_to_xml("node_order", testcase["node_order"]) + self.content
            self.content = self.content + self.content_to_xml("keywords", testcase["keywords"])
            self.content = self.content_to_xml("name", testcase["name"]) + self.content
            self.content = self.content + "</testcase>"
            self.content_list.append(self.content)
            self.content = ""
        self.content = "".join(self.content_list)
        self.content = '<testsuite name="' + self.testsuite + '">'+ self.content + "</testsuite>"
        self.content = '<?xml version="1.0" encoding="UTF-8"?>' + self.content
        self.write_to_file()

    def write_to_file(self):
        cp = open("test.xml", "w")
        cp.write(self.content.encode('utf-8'))
        cp.close()

if __name__=='__main__':
    test = operate()
    test.xlsx_to_dic()
    test.dic_to_xml()