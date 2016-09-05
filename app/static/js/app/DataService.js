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
    this.cvResults = [];
    this.test = true;

    var clearData = function () {

    };

    this.getDataItems = function () {
        return self.dataItems;
    };

    this.getCvResults = function () {
        return self.cvResults;
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
                $rootScope.$emit(EventConstants.eventDataLoadFinished);
            })
            .error(function (data, status, header, config) {
                console.log("error: " + status)
            });
    };

    this.loadRealx = function () {
        var request = $http({
            method:'GET',
            url:'api/load_real_x',
            params: {'xpath': '/Users/hzhehui/Downloads/process_data_result/DA/X.txt'}
        });

        request.success(function (data, status, headers, config) {
                if(data.code == 1) {
                    self.dataItems = data.data.items;
                    $rootScope.$emit('eventRealxLoadFinished');
                }
                else if(data.code == 0){
                    console.log('error_code:' +  data.code + ' msg: ' + data.msg);
                }
            })
            .error(function (data, status, headers, config) {

            })
    };
    
    this.computeError = function (dataId) {
        var request = $http({
            method:'GET',
            url:'api/compute_error',
            params: {'id': dataId}
        });

        request.success(function (data, status, headers, config) {
                if(data.code == 1){
                    x_compute = data.data.x_compute;
                    x_error = data.data.x_error;
                    self.dataItems[dataId - 1]['x_compute'] = x_compute;
                    self.dataItems[dataId - 1]['x_error'] = x_error;
                    $rootScope.$emit('eventComputeErrorFinished');

                }
            })
            .error(function (data, status, headers, config) {

            })
    };

    this.computeMultipleXError = function (computeErrorArray) {

        // update data of service
        for (var index in computeErrorArray){
            self.dataItems[index]['isSelectedForCompErr'] = true;
        }

        var request = $http({
            method: 'GET',
            url: 'api/compute_multiple_error',
            params: {'idArray': angular.toJson(computeErrorArray)}
        });

        request.success(function (data, status, headers, config) {
                if(data.code == 1){
                    compute_results = data.data.compute_results;
                    console.log("compute_results: " + compute_results);
                    for(var i = 0; i < compute_results.length; i++){
                        var item = compute_results[i];
                        self.dataItems[item.id - 1]['x_compute'] = item.x_compute;
                        self.dataItems[item.id - 1]['x_error'] = item.x_error;
                        self.dataItems[item.id - 1]['hasComputed'] = true;
                    }
                    $rootScope.$emit('eventComputeMultipleErrorFinished');
                }
            })
            .error(function (data, status, headers, config) {

            });
    };

    this.computeCV = function () {

        var request = $http({
            method: 'GET',
            url: 'api/compute_cv',
        });

        request.success(function (data, status, headers, config){

                if(data.code == 1){
                    self.cvResults = data.data.cv_results;
                    console.log("cvresults: " + self.cvResults);
                    $rootScope.$emit('eventComputeCVFinished');
                }
                else{

                }
            })
            .error(function (data, status, headers, config) {

            });
    };

}

DataService.prototype = Object.create(BaseService.prototype);
DataService.prototype.constructor = DataService;

app.factory('DataService', ['$rootScope', '$http', function ($rootScope, $http) {

    var service  = new DataService($rootScope, $http);
    return service;
}])