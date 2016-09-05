# -*- coding: utf-8 -*-
from app.processLogic.ExcelProcessor import ExcelProcessor
from app.processLogic.DataModel import *
from app.processLogic.logisticCurveFit import *
import sys
import os
import shutil

default_store_path = "/Users/hzhehui/PycharmProjects/Data"
#Ui_Form,QtBaseClass = uic.loadUiType(ui_file)

#delegate: make all item show in cental


class EasyProccessor():
    def __init__(self):
        self.dataItems = []
        self.logisticCurveFit = LogisticCurveFit()
        pass

    def cv_compute(self):
        pass

    def save_data(self):
        pass

    def exit(self):
        pass

    '''DA:数据预处理, 首先需要选择原数据路径'''
    def pre_process_xls_data(self, process_data_path):
        #load 此目录下的所有xls文件
        excelProcessor = ExcelProcessor(process_data_path)
        excelProcessor.pre_process_all_excel_files()
        return

    '''导入x真实浓度, 首先要选择'''
    def load_xreal_value(self, xreal_file):
        file = open(xreal_file)
        xreal_array = []
        for line in file:
            if line == '\n' or line == '\r\n':
                continue
            xreal_array.append(line)

        if len(xreal_array) != len(self.dataItems):
            return None

        #导入真实浓度
        for index in range(0, len(xreal_array)):
            self.dataItems[index]['x_real'] = xreal_array[index]

        return self.dataItems


    def readdata(self):
        file = open("sample.txt")
        self.array_x_real = []
        self.array_y_real = []
        for line in file:
            array = line.split('\t')
            self.array_x_real.append(int(array[0]))
            self.array_y_real.append(float(array[1]))

    '''
    slot filed
    '''
    def curve_fit(self, is_all):

        self.array_x_real = []
        self.array_y_real = []

        for index in range(0, len(self.dataItems)):
            self.array_x_real.append(float(self.dataItems[index]['x_real']))
            self.array_y_real.append(float(self.dataItems[index]['t_xinhao']))

        print(self.array_x_real)
        print(self.array_y_real)
        #logisticCurveFilt = LogisticCurveFit(self.array_x_real, self.array_y_real)

        self.logisticCurveFit.initdata(self.array_x_real, self.array_y_real)

        save_path = '%s/data/result/logistic.png' % '/Users/hzhehui/Downloads/process_data_result/DA'
        self.logisticCurveFit.curvefit(save_path)
        return save_path

    '''
    load & reload(不同批次), 如果是reload, 需要清空原有数据,重新加载新数据
    '''
    def load_data(self, path):
        #call exe to process
        self.dataItems = []
        result_file_path = '%s/data/result/testResult_DUAN.txt' % path

        if os.path.exists(result_file_path) is False:
            return False

        file = open(result_file_path)
        dataItems = []
        index = 0
        for line in file:
            #dataItem = DataModel().generate_from_stringline(line)
            index += 1
            dataItem = DataModel().generate_json_from_stringline(line)
            dataItem['id'] = index
            self.dataItems.append(dataItem)

        return self.dataItems

    def compute_error(self, dataId):
        print(dataId)
        x_real = float(self.dataItems[dataId - 1]['x_real'])
        y_real = float(self.dataItems[dataId - 1]['t_xinhao'])
        x_compute, x_error = self.logisticCurveFit.compute_error(x_real, y_real)
        if math.isnan(x_compute) or math.isnan(x_error):
            x_compute = 'nan'
            x_error = 'nan'
        self.dataItems[dataId - 1]['x_compute'] = x_compute
        self.dataItems[dataId - 1]['x_error'] = x_error
        return x_compute, x_error

    def cv_compute(self):
        # if self.expirement_group == "NE":
        #     save_path = '%s/data/result/cv_info.xls' % self.ne_root_path
        # elif self.expirement_group == 'DA':
        #     save_path = '%s/data/result/cv_info.xls' % self.da_root_path
        save_path = '%s/data/result/logistic.png' % '/Users/hzhehui/Downloads/process_data_result/DA'
        cv_results = self.logisticCurveFit.compute_cv(save_path)
        return cv_results




