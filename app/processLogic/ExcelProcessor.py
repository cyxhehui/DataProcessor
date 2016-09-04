import xlrd
import os


class ExcelProcessor(object):

    def __init__(self, root_path):
        #self.store_path = ""
        self.root_path = root_path

    def get_all_excel_files(self):
        all_files = os.listdir(self.root_path)
        excel_files = []
        for file in all_files:
            if os.path.splitext(file)[1] == '.xls':
                excel_files.append(file)

        print(excel_files)
        return excel_files

    def open_excel(self, excel_file):
        try:
            data = xlrd.open_workbook(excel_file)
            return data
        except Exception as e:
            print(str(e))

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
        for col in range(1, ncols - 1):
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

        #get file name: x_y.dat
        if group_number < 10:
            dst_file = '%s/DA_0%d_00%d.dat' % (sub_dir, group_number, col)
        else:
            dst_file = '%s/DA_%d_%d.dat' % (sub_dir, self.experiment_group, col)
        file = open(dst_file, "w+")
        for item in data:
            line = '%f%s' % (item , '\r\n')
            file.write(line)
        file.close()


if __name__ == "__main__":
    processor = ExcelProcessor("/Users/hzhehui/PycharmProjects/DA_exp")
    processor.pre_process_all_excel_files()