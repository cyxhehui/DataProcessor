import xlrd
from xlwt import Workbook
import os
import re


class ExcelProcessor(object):

    def __init__(self, root_path = None):
        #self.store_path = ""
        self.root_path = root_path
        self.write_book = Workbook()

    def get_all_excel_files(self):
        all_files = os.listdir(self.root_path)
        excel_files = []
        for file in all_files:
            if re.match("批\d*.xls", file) is not None:
                excel_files.append(file)

        print(excel_files)
        return excel_files

    def open_excel(self, excel_file):
        try:
            data = xlrd.open_workbook(excel_file)
            return data
        except Exception as e:
            print(str(e))

    def init_cv_sheet(self):
        sheet_name = "cv_info"
        sheet = self.write_book.add_sheet(sheet_name)
        row = sheet.row(0)
        row.write(0, "X")
        row.write(1, "Y-反应值")
        row.write(2, "Y-平均值")
        row.write(3, "CV（%）")
        return  sheet

    def init_all_data_sheet(self):
        sheet_name = "all_data"
        sheet = self.write_book.add_sheet(sheet_name)
        row = sheet.row(0)
        row.write(0, "文件名称")
        row.write(1, "T线信号比")
        row.write(2, "x真实浓度")
        row.write(3, "x计算浓度")
        row.write(4, "浓度误差(%)")
        return sheet

    def write_all_data_info(self, sheet, row_index, file_name, y_value, x_real_value, x_predict_value, x_error_value):
        row = sheet.row(row_index)
        row.write(0, file_name)
        row.write(1, y_value)
        row.write(2, x_real_value)
        row.write(3, x_predict_value)
        row.write(4, x_error_value)

    def write_cv_info(self, sheet, start_row, x_class_array, y_class_arry, cv_info_for_class):

        start = start_row
        for index in range(0, len(x_class_array)):
            row = sheet.row(start)
            start += 1
            row.write(0, str(x_class_array[index]))
            row.write(1, str(y_class_arry[index]))
        row.write(2, str(cv_info_for_class[1]))
        row.write(3, str(cv_info_for_class[2]))

    def save_book(self, excel_file):
        self.write_book.save(excel_file)


    def extract_data_byindex(self, excel_file, by_index = 1):
        #从文件名中提取批次号, 不过首先要确保文件名命名正确, 需要正则表达式之类, 一开始在确定excel文件时,就确保正确性
        group_number = int(excel_file[1])
        file_path = ("%s/%s") % (self.root_path, excel_file)
        data = self.open_excel(file_path)
        table = data.sheet_by_index(by_index) #select the 2nd table
        nrows = table.nrows
        ncols = table.ncols

        # make sure the excel file is integrated , it contains 350 items.
        if nrows != 350:
            print("Invalid excel file")

        #get each coloum data
        for col in range(1, ncols):
            col_data = table.col_values(col)
            if len(col_data) != 350:
                print("Invalid excel file")
            print(col_data)
            self.store_data_in_file(group_number, col_data, col)

    def pre_process_all_excel_files(self):
        excel_files = self.get_all_excel_files()
        if len(excel_files) == 0:
            return
        for excel_file in excel_files:
            self.extract_data_byindex(excel_file)

    '''保存文件,在root_path下创建data目录,然后以DA_01_001.dat的形式保存'''
    def store_data_in_file(self, group_number, data, col):
        sub_dir = '%s/data' % (self.root_path)
        if os.path.exists(sub_dir) == False:
            os.makedirs(sub_dir)

        if col < 10:
            col_text = '00%d' % col
        elif col < 100:
             col_text = '0%d' % col
        else:
            col_text = '%d' % col

        if group_number < 10:
            group_text = '0%d' % group_number
        else:
            group_text = '%d' % group_number

        dst_file = '%s/DA-%s-%s.dat' % (sub_dir, group_text, col_text)
        #get file name: x_y.dat
        file = open(dst_file, "w+")
        for item in data:
            line = '%f%s' % (item , '\r\n')
            file.write(line)
        file.close()


if __name__ == "__main__":
    processor = ExcelProcessor("/Users/hzhehui/PycharmProjects/DA_exp")
    processor.pre_process_all_excel_files()