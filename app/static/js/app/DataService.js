/**
 * Created by hzhehui on 4/9/2016.
 */

//base class for all services. This allows easier listening for events
function BaseService($rootScope) {
    var listeners = {};

    this.registerListener = function(controller, event, func) {
        if (!listeners[controller]) {
            listeners[controller] = {};
        }
        if (!listeners[controller][event]) {
            listeners[controller][event] = [];
        }
        var unregister = $rootScope.$on(event, func);
        listeners[controller][event].push(unregister);
    };

    this.unregisterListeners = function(controller) {
        if (listeners[controller]) {
            for (var event in listeners[controller]) {
                if (listeners[controller].hasOwnProperty(event)) {
                    for (var i = 0; i < listeners[controller][event].length; ++i) {
                        listeners[controller][event][i]();
                    }
                }
            }
            delete listeners[controller];
        }
    };

    this.unregisterListener = function(controller, event) {
        if (listeners[controller][event]) {
            for (var i = 0; i < listeners[controller][event].length; ++i) {
                listeners[controller][event][i]();
            }
            delete listeners[controller][event];
        }
    };
}

function DataService($rootScope, $http){

    BaseService.call(this, $rootScope);

    var self = this;
    this.dataItems = [];
    this.test = true;

    var clearData = function () {

    };

    this.getDataItems = function () {
        return self.dataItems;
    };

    this.dataLoad = function (selectedDataSource) {
        var params;
        if (selectedDataSource == 'DA'){
            params = {'datasource': 'DA', 'path': "/Users/hzhehui/Downloads/process_data_result/DA"};
        }
        else if(selectedDataSource == 'NE'){
            params = {'datasource': 'NE', 'path': "/Users/hzhehui/Downloads/process_data_result/NE"};
        }

        var request = $http({
                method:'GET',
                url:'api/data_load',
                params: params,
        });

        request.success(function (data, status, headers, config) {
                self.test = false;
                for(var i = 0; i < data.data.items.length; i++)
                self.dataItems.push(data.data.items[i]);
                $rootScope.$emit("dataLoadFinish");
            })
            .error(function (data, status, header, config) {
                console.log("error: " + status)
            });
    };

    this.loadRealx = function () {

    };

}

DataService.prototype = Object.create(BaseService.prototype);
DataService.prototype.constructor = DataService;

app.factory('DataService', ['$rootScope', '$http', function ($rootScope, $http) {

    var service  = new DataService($rootScope, $http);
    return service;
}])