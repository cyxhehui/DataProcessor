//! alert.js
//! version : 1.0.0
//! authors : nick
//! 公共组件

var util = util || {};

(function ($) {
    "use strict";

    var alert = {};

    alert.DEFAULT_OPTION = {
        fadeIn: 500, // 弹出框fade动画持续时间
        fadeDuration: 4000, // 弹出框停留时间
        fadeOut: 500 // 淡出动画持续时间
    };

    /**
     * 此方法可详细定制alert各项目参数
     * @param priority string - alert弹出层属性
     * @param msg string - 要弹出的消息
     * @param opts Object - Options to set the prompt
     */
    alert.trigger = function (priority, msg, opts) {
        if (typeof opts !== "object") {
            opts = {};
        }
        $.extend(alert.DEFAULT_OPTION, opts);

        $(document).trigger("add-alerts", [
            {
                'message': msg,
                'priority': priority,
                'fadeIn': alert.DEFAULT_OPTION.fadeIn,
                'fadeDuration': alert.DEFAULT_OPTION.fadeDuration
            }
        ]);
    };

    alert.error = function (msg, opts) {
        alert.trigger("error", msg, opts);
    };

    alert.success = function (msg, opts) {
        alert.trigger("success", msg, opts);
    };

    util.alert = alert;
})(jQuery);