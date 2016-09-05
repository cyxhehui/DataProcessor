import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import pandas as pd
import math

from app.processLogic.cvDataModel import *
from app.processLogic.ExcelProcessor import ExcelProcessor
import os


class LogisticCurveFit:
    def __init__(self):
        self.array_x = []
        self.array_y = []
        self.array_y_p = []
        self.params_abcd = []

    def initdata(self, array_x_param, array_y_param):
        self.array_x = array_x_param
        self.array_y = array_y_param

    def compute_r2(self):
        # compute array_y_p
        for x in self.array_x:
            y = self.peval(x, self.params_abcd[0])
            self.array_y_p.append(y)

        # compute ava_y
        sum_y = 0
        sum1 = 0
        sum2 = 0
        r2 = 0
        index = 0
        for y in self.array_y:
            sum_y = sum_y + y
        y_a = sum_y / len(self.array_y)

        for y in self.array_y:
            y_p = self.array_y_p[index]
            index += 1
            sum1 += (y - y_a) ** 2
            sum2 += (y_p - y_a) ** 2

        r2 = sum2 / sum1
        print(r2)
        return r2

    def compute_error(self, x_real, y):
        A, B, C, D = self.params_abcd[0]
        x_predict = C * (((A - y) / (y - D)) ** (1/B))
        error = abs(100 *(x_predict - x_real) / x_real)
        return x_predict, error

    def get_x_array_for_plot(self):
        df = pd.DataFrame({'x': self.array_x, 'y': self.array_y})
        grouped = df['y'].groupby(df['x'])
        x_classify = []
        y_classify = []

        for (x, y) in grouped:
            x_classify.append(x)

        return x_classify

    def compute_cv(self, save_path):
        cv_results = []

        excelProcessor = ExcelProcessor()
        df = pd.DataFrame({'x': self.array_x, 'y': self.array_y})
        grouped = df['y'].groupby(df['x'])
        x_classify = []
        y_classify = []

        start = 0
        sheet = excelProcessor.init_cv_sheet()
        for (x, y) in grouped:
            length = len(y)
            array_y = y.values
            for index in range(0, length):
                x_classify.append(x)
                y_classify.append(float("%.5f" % array_y[index]))

            start += length
            cv_info = []
            x_classify_sub = x_classify[start - length : start]
            y_classify_sub = y_classify[start - length : start]
            cv_info.append(start)
            cv_info.append(float("%.5f" % np.mean(y_classify_sub)))
            #cv_info.append(100 * np.std(y_classify_sub)/np.mean(y_classify_sub) )
            stdev = 0
            for i in range (0, len(y_classify_sub)):
                stdev += (y_classify_sub[i] - cv_info[1])**2
            stdev_val = (stdev /(len(y_classify_sub) - 1))**(0.5) / cv_info[1]
            cv_info.append(float("%.5f" % stdev_val))

            cv_results_part = CVDataModel().generate_cv_data(x_classify_sub, y_classify_sub, cv_info)
            for item in cv_results_part:
                cv_results.append(item)

            print(stdev_val)

            excelProcessor.write_cv_info(sheet, start - length + 1, x_classify_sub, y_classify_sub, cv_info)

        excelProcessor.save_book(save_path)
        return cv_results

    def logistic4(self, x, A, B, C, D):
        """4PL lgoistic equation."""
        return ((A - D) / (1.0 + ((x / C) ** B))) + D

    def residuals(self, p, y, x):
        """Deviations of data from fitted 4PL curve"""
        A, B, C, D = p
        err = y - self.logistic4(x, A, B, C, D)
        return err

    def peval(self, x, p):
        """Evaluated value at x with current parameters."""
        A, B, C, D = p
        return self.logistic4(x, A, B, C, D)

    def curvefit(self, save_path):
        # Initial guess for parameters
        p0 = [1,1,1,1]

        self.params_abcd = leastsq(self.residuals, p0, args=(self.array_y, self.array_x))
        r2 = self.compute_r2()

        y_compute = self.peval(self.array_x, self.params_abcd[0])
        print (y_compute)
        #plot result
        x_for_plot = self.get_x_array_for_plot()
        plt.plot(x_for_plot, self.peval(x_for_plot, self.params_abcd[0])[0:17])
        plt.legend(['Fit'], loc='upper left')
        for i, (param, est) in enumerate(zip('ABCDR', self.params_abcd[0])):
            plt.text(60, 1.6 - i * 0.2, 'est(%s) = %.5f' % (param, est))
#
        plt.title('Y = %.5f / [1.0 + (x / %.5f) ** %.5f)] + %.5f' % (self.params_abcd[0][0] -self.params_abcd[0][3], self.params_abcd[0][2], self.params_abcd[0][1], self.params_abcd[0][3]))
        plt.text(35, 1.0, ' r^2 = %.5f' % r2)

        plt.savefig(save_path)
        plt.cla()
        plt.clf()
        plt.close()

def readdata(array_x_param, array_y_param):
    file = open("sample.txt")
    for line in file:
        array = line.split('\t')
        array_x_param.append(int(array[0]))
        array_y_param.append(float(array[1]))


if __name__ == "__main__":
    array_x_param = []
    array_y_param = []
    readdata(array_x_param, array_y_param)
    curveFit = LogisticCurveFit()
    curveFit.initdata(array_x_param, array_y_param)
    curveFit.curvefit("test.png")
    curveFit.compute_cv("test.xls")
    error = curveFit.compute_error(10, 1.11910)
    print('error = %.5f' % error)


