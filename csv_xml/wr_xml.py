#coding:utf-8
from xml.dom.minidom import Document
import xlrd
import os
import ConfigParser
class write_xml(object):
    def __init__(self):
        self.testlink_datas=['tag','name','node_order','details','internalid','externalid','summary','steps','expectedresults']
        self.work_path=os.path.abspath(os.getcwd())+ '\\config.ini'
      #  self.filename_csv=filename_csv
    def __str__(self):
        """
        打印testlink_csv表的字段名
        :return: testlink_datas
        """
        return self.testlink_datas

    def fileDict(self,work_path,default_index=0):
        #只提取一张默认index为0的表
        #TODO 同表多sheet时需要额外处理
        #默认表testlink第一行为表头数据，第二行为case数据
        rs=xlrd.open_workbook(work_path)
        rs_sheet=rs.sheet_by_index(default_index)
        csv_data=[]
        for row in range(1,rs_sheet.nrows):
            row_data=[]
            for col in range(0,rs_sheet.ncols):
                unit_data=rs_sheet.cell_value(row,col)
                row_data.append(unit_data)
            csv_data.append(row_data)
        return csv_data

    # 将self.fileDict中的信息写入本地xml文件，参数filename是xml文件名
    def writeInfoToXml(self, filename_xml='default.xml'):
        # 创建dom文档，创建根节点为Testcases
        # 私有方法
        #获取配置中的文件名字
        def readcf():
            cf = ConfigParser.ConfigParser()
            with open(self.work_path) as cfconfig:
                cf.readfp(cfconfig)
            filename_csv = cf.get('data', 'test_path')
            return filename_csv
        path=readcf()
        if os.path.isfile(path):
            filname=os.path.basename(path)
            filename_xml=filname.split('.')[0]+'.xml'
        doc = Document()
        testcases = doc.createElement('testsuite')
        doc.appendChild(testcases)

        # 依次将Dict中的每一组元素提取出来，创建对应节点并插入dom树
        for list_data in self.fileDict(path):
            #TODO 针对testlink csv导出文件8个字段写入到Testcase下
            # tag, name, node_order, details, internalid, externalid, summary, steps, expectedresults
            tag, name, node_order, details, internalid, externalid, summary, steps, expectedresults=list_data
            # 每一组信息先创建节点<Testcase>，然后插入到父节点<testcases>下
            testcase= doc.createElement('testcase')
            testcase.setAttribute('name','TC-'+str(self.fileDict(path).index(list_data)).zfill(3))
            testcases.appendChild(testcase)
            """
            # 创建节点<tag>
            tag = doc.createElement(self.testlink_datas[0])
            tag_text = doc.createTextNode(tag)
            tag.appendChild(tag_text)
            testcase.appendChild(tag)
            """
            # 创建节点<tag>
            self.create_ele(doc,testcase,self.testlink_datas[0],tag)
            # 创建节点<name>
            self.create_ele(doc,testcase,self.testlink_datas[1],name)
            # 创建节点<node_order>
            self.create_ele(doc,testcase,self.testlink_datas[2],node_order)
            #创建节点<details>
            self.create_ele(doc,testcase,self.testlink_datas[3],details)
            #创建节点<internalid>
            self.create_ele(doc,testcase,self.testlink_datas[4],internalid)
            #创建节点 <externalid>
            self.create_ele(doc,testcase,self.testlink_datas[5],externalid)
            #创建节点 <summery>
            self.create_ele(doc,testcase,self.testlink_datas[6],summary)
            #创建节点 <steps>
            self.create_ele(doc,testcase,self.testlink_datas[7],steps)
            #创建节点 <expectedresult>
            self.create_ele(doc,testcase,self.testlink_datas[8],expectedresults)

        # 将dom对象写入本地xml文件
        with open(filename_xml, 'w') as f:
            f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))
        return  True

    #封装创建节点，传入doc、根节点
    def create_ele(self,doc,testcase,element,element_text):
        if isinstance(element_text,float):
            element_text=str(element_text)
        elif isinstance(element_text,int):
            element_text=str(element_text)
        element_text=element_text.replace('\n','')
        count = doc.createElement(element)
        count_text = doc.createTextNode(element_text)
        count.appendChild(count_text)
        testcase.appendChild(count)

if __name__=="__main__":
    write_xml().writeInfoToXml()
