class CVDataModel:

    def __init__(self):
        self.cvResults = []


    def generate_cv_data(self, x_class_sub, y_class_sub, cv_info):
        for index in range(0, len(x_class_sub)):
            cv_item = {'x_real': x_class_sub[index],
                       'y_real': y_class_sub[index],
                       'y_mean': '',
                       'cv': '',
                       'y_compute': '',
                       'y_error': '',
                       }
            if index == len(x_class_sub) - 1:
                cv_item['y_mean'] = cv_info[1]
                cv_item['cv'] = cv_info[2]

            self.cvResults.append(cv_item)

        return self.cvResults
