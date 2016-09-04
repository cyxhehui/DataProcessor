# -*- coding: utf-8 -*-

class DataModel:

    def __init__(self):
        self.file_name = ""
        self.c_location = ""
        self.t_locaation = ""
        self.c_huidu = ""
        self.t_huidu = ""
        self.c_zao = ""
        self.t_zao = ""
        self.c_xinhao = ""
        self.t_xinhao = ""
        self.x_real = ""
        self.x_compute = ""
        self.x_error = ""
        self.isSelected = False
        pass


    def generate_from_stringline(self, line):

        if len(line) != 0:
            pieces = line.split(",")
            # process pieces[0], 提取文件名
            split_array = pieces[0].split("\\")
            dat_file = split_array[len(split_array) - 1]
            print(dat_file)
            pieces[0] = dat_file
            print(pieces[0])
            dataItem = DataModel()
            dataItem.file_name = pieces[0]

            dataItem.c_location = pieces[1]
            dataItem.t_locaation = pieces[2]
            dataItem.c_huidu = pieces[3]
            dataItem.t_huidu = pieces[4]
            dataItem.c_zao = pieces[5]
            dataItem.t_zao = pieces[6]
            dataItem.c_xinhao = pieces[7]
            dataItem.t_xinhao = pieces[8]
            # self.x_real = pieces[10]
            # self.x_compute = pieces[11]
            # self.x_error = pieces[12]
            return dataItem

    def generate_json_from_stringline(self, line):

        if len(line) != 0:
            pieces = line.split(",")
            # process pieces[0], 提取文件名
            split_array = pieces[0].split("\\")
            dat_file = split_array[len(split_array) - 1]
            print(dat_file)
            pieces[0] = dat_file
            print(pieces[0])
            temp = {'file_name': pieces[0],
                    'c_location': pieces[1],
                    't_location': pieces[2],
                    'c_huidu': pieces[3],
                    't_huidu': pieces[4],
                    'c_zao': pieces[5],
                    't_zao': pieces[6],
                    'c_xinhao': pieces[7],
                    't_xinhao': pieces[8],
                    'x_real': '',
                    'x_compute': '',
                    'x_error': '',
                    'isSelected': False}

            return temp
        else:
            return None