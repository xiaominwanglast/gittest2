#coding:utf-8
import xlrd
import os
import re
import ConfigParser
from xlutils.copy import copy
class WR_CSV(object):
    """
    将Testlink 转换成csv/xls/xlsx
    """
    def __init__(self):
        self.work_path=self.getconfigpath
        self.result_path=os.path.abspath(os.getcwd())+'\\xml_csv.xls'
        self.list_data=[]
        #
        self.keywords={"testsuit_name":u'项目名','testcase_name':u'用例名',"version":u'版本',
                       "summary":u'描述',"preconditions":u'前提', "importance":u"重要性",'step_number':u'步骤序号','actions':u'动作描述','expectedresults':u'期望结果', "keywords":u'关键词'}
        if not os.path.exists(self.result_path):
            with open(self.result_path,'wb') as fs:
                fs.write()

    def __str__(self):
        """
        返回测试路径
        :return:
        """
        return self.work_path

    @property
    def getconfigpath(self):
        CF=ConfigParser.ConfigParser()
        config_path=os.path.abspath(os.getcwd())+'\\config.ini'
        with open(config_path,'rb') as fs:
            CF.readfp(fs)
        return CF.get('data','xml_path')

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


    @classmethod
    def dill_data(cls,data):
        """
        :param data: 需要处理数据
        :return: 返回处理后的数据
        """
        return data.replace('![','').replace('<p>','').replace('</p>','').replace(']]','').replace('CDATA[','')

    #封装类方法
    @classmethod
    def get_values(cls,rule,test_data):
        test_result=re.findall(rule,test_data)
        if test_result:
            if len(test_result)==1:
                if 'testsuite' in rule or 'testcase' in rule or 'version' in rule or 'step_number' in rule or 'actions' in rule or 'expectedresults' in rule or 'keyword' in rule:

                    return test_result[0]
                else:
                    return test_result
            else:
                return test_result
        else:
            return ''

    def content_to_xml(self, key, value=None):
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

    def create_csvfile(self):
        rs=xlrd.open_workbook(self.result_path)
        rs_sheet=rs.sheet_by_index(0)
        print rs_sheet.ncols
        """
        rs_copy=copy(rs)
        col=0
        for value in self.keywords.values():
            print value
            rs_copy.get_sheet(0).write(0,col,value)
            col+=1
        rs_copy.save(self.result_path)
        """
if __name__=='__main__':
    WR_CSV().write_xml_csv()