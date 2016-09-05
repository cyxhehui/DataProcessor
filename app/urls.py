from django.conf.urls import url, include
from app.base_views import base_view


urlpatterns = [
    url(r'^$', base_view.f_index, name='f_index'),
    url(r'^api/pre_process_data', base_view.pre_process_data, name='pre_process_data'),
    url(r'^api/data_load', base_view.data_load, name='data_load'),
    url(r'^api/load_real_x', base_view.load_real_x, name='load_real_x'),
    url(r'^api/curve_fit', base_view.curve_fit, name='curve_fit'),
    url(r'^api/compute_cv', base_view.compute_cv, name='compute_cv'),
    url(r'^api/compute_error', base_view.compute_error, name='compute_error'),
    url(r'^api/compute_multiple_error', base_view.compute_multiple_error, name='compute_multiple_error'),
    url(r'^api/save', base_view.save, name='save'),

    # 处理curve结果相关
    url(r'^curve_result.html$', base_view.show_curve_result, name='show_curve_result'),

    # 处理cv结果相关
    url(r'^cv_result.html$', base_view.show_cv_result, name='show_cv_result'),
]