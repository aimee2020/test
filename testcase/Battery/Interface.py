# 测试结论单独写一个方法
# author:lyy
# date:2020-12-30 将
import csv

import demjson
import requests


class Interface():
    def __init__(self):
        self.TestReportDict = {}
        self.BaseUrl = ''
        self.token = ''
        # self.client_id = ''
        self.secret = ''
        self.ReadGlobal()

    def ReadGlobal(self):
        # global = {}
        self.BaseUrl = ''
        self.Param = {}
        DataFilePath = r"../global.csv"
        Count = 0
        with open(DataFilePath, "r", encoding='UTF-8') as DataFile:
            table = csv.reader(DataFile)
            next(table)
            row = next(table)
            self.BaseUrl = row[0]
            self.header = row[3]

    # 读取测试用例中的数据
    def ReadTestData(self):
        # global = self.ReadGlobal();

        TestDataDic = {}
        DataFilePath = r"TestData.csv"
        self.CreateReport()
        with open(DataFilePath, "r", encoding='UTF-8') as DataFile:
            DataTable = csv.reader(DataFile)
            Count = 0
            for row in DataTable:
                if Count > 0:
                    TestDataDic['InterfaceName'] = row[1]
                    TestDataDic['Url'] = self.BaseUrl + row[3]
                    TestDataDic['header'] = self.header
                    TestDataDic['Result'] = row[4]
                    RequestMethod = row[2]
                    TestDataDic['param'] = row[6]
                    TestDataDic['RequestMethod'] = RequestMethod
                    self.RequestTest(TestDataDic)
                Count += 1

    def RequestTest(self, TestDataDic):
        url = TestDataDic['Url']
        param = TestDataDic['param'].encode()
        headers = eval(TestDataDic['header'])
        if TestDataDic['RequestMethod'] == "post":
            r = requests.post(url, data=param, headers=headers)
            response = r.text
        elif TestDataDic['RequestMethod'] == "get":
            r = requests.get(url=url, headers=headers, verify=False, timeout=10)
            response = r.text
            # print(r.text)

        else:
            r = requests.delete(url=url, headers=headers, data=param)
            response = r.text
        responsecode = demjson.decode(response)
        code = responsecode['code']
        # print(code)
        # print(type(code))
        # print(type(responsecode['code']))
        # print(TestDataDic['Result'])
        # print(code == int(TestDataDic['Result']))
        self.TestReportDict["测试接口名称"] = TestDataDic['InterfaceName']
        self.TestReportDict["测试接口地址"] = TestDataDic["Url"]
        if code == int(TestDataDic['Result']):
            print(TestDataDic['InterfaceName'] + "测试成功")
            self.TestReportDict["测试结论"] = TestDataDic['InterfaceName'] + "测试成功"
        else:
            print(TestDataDic['InterfaceName'] + "测试失败")
            self.TestReportDict["测试结论"] = TestDataDic['InterfaceName'] + "测试失败"
        self.TestReportDict["测试响应结果"] = str(response)
        self.SaveReport()

    # 创建测试报告并生成标题
    def CreateReport(self):

        self.ReportPath = r"TestReport.csv"
        self.ReportFile = open(self.ReportPath, "w", encoding='UTF-8')
        self.ReportFile.write("测试接口名称" + "," + "测试接口地址" + "," + "测试结论" + "," + "测试响应结果" + "\n")
        self.ReportFile.close()

    def SaveReport(self):
        self.ReportFile = open(self.ReportPath, "a", encoding='UTF-8')
        for key, value in self.TestReportDict.items():
            self.ReportFile.write(str(value) + ",")
        self.ReportFile.write("\n")
        self.ReportFile.close()


if __name__ == '__main__':
    InterfaceObj = Interface()
    InterfaceObj.ReadTestData()
