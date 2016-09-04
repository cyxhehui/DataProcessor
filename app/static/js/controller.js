/**
 * Created by hzhehui on 3/9/2016.
 */

app.controller('helloCtrl', function($scope, $http){

    $scope.name = "hehui";

    $scope.dataSources = ['NE', 'DA'];
    $scope.selectedDataSource = 'DA';
    $scope.changeDataSource = function () {
        $scope.selectedDataSource = this.selectedDataSource;
        console.log("select source:" + $scope.selectedDataSource);
    };

    $scope.hasData = function () {
        if($scope.dataItems)
            return true;
        else
            return false;
    }

    $scope.selectAll = function () {
        if($scope.dataItems){

            if($scope.isSelectAll){
                console.log("ts");
                for(var i = 0; i < $scope.dataItems.length; i++){
                    $scope.dataItems[i].isSelected = true;
                }
            }
            else{
                console.log("ts1");
                for(var i = 0; i < $scope.dataItems.length; i++){
                    $scope.dataItems[i].isSelected = false;
                }
            }
        }
    };

    //request with filepath, response: process successful or fail.
    $scope.preprocessData = function () {

        console.log("preprocess data")
        var request = $http({
            method: 'GET',
            url: 'api/pre_process_data',
            params: {path: "/Users/hzhehui/Downloads/process_data_result/DA"}
        });
        request.success(function (data, status, headers, config) {

                console.log("staus: " + status + data.code + data.msg)

            })
            .error(function (data, status, header, config) {
                console.log("error: " + status)
            });
    };

    // re-process data and show in table
    // for DA, no need to open fileDialog, but for NE, need to do that ,and let user choose the dir
    $scope.dataLoad = function () {
        console.log("load data");
        var params;
        if ($scope.selectedDataSource == 'DA'){
            params = {'datasource': 'DA', 'path': "/Users/hzhehui/Downloads/process_data_result/DA"};
        }
        else if($scope.selectedDataSource == 'NE'){
            params = {'datasource': 'NE', 'path': "/Users/hzhehui/Downloads/process_data_result/NE"};
        }

        var request = $http({
                method:'GET',
                url:'api/data_load',
                params: params,
            });

        request.success(function (data, status, headers, config) {
                $scope.dataItems = data.data.items;
            })
            .error(function (data, status, header, config) {
                console.log("error: " + status)
            });

    };
    
    $scope.loadRealx = function () {

        console.log('load real x');

        var request = $http({
            method:'GET',
            url:'api/load_real_x',
            params: {'xpath': '/Users/hzhehui/Downloads/process_data_result/DA/X.txt'}
        });

        request.success(function (data, status, headers, config) {
                if(data.code == 1) {
                    $scope.dataItems = data.data.items;
                    console.log('status :' + status + 'msg: ' + data.msg);
                }
                else if(data.code == 0){
                    console.log('error_code:' +  data.code + ' msg: ' + data.msg);
                }
            })
            .error(function (data, status, headers, config) {

            })
    };

    $scope.curveFit = function () {
        console.log('curve fit');
        var selected_array = [];
        var i = 0;
        for(i = 0; i < $scope.dataItems.length; i++){
            if($scope.dataItems[i].isSelected){
                selected_array.push(i);
            }
        }
        console.log(selected_array);
        console.log(angular.fromJson($scope.dataItems));

        if(selected_array.length == 0){

            //error: alter
            console.log("please choose data to curve");
        }

        var request = $http({
            method:'GET',
            url:'show_curve.html/',
            params:{'selecteditems': angular.toJson(selected_array)}
        });

        request.success(function (data, status, headers, config) {
                console.log('status:' + status + 'msg: ' + data.msg);
                if(data.code == 1) {
                    console.log('status :' + status + 'msg: ' + data.msg);
                    console.log('image:' + data.data.curveimage);
                    $http({
                        method:'GET',
                        url:'api/show_curve_result',
                        params:{'curveimage':data.data.curveimage}
                    }).success(function (data, status, headers, config) {

                    }).error(function (data, status, headers, config) {

                    })
                }
                else if(data.code == 0){
                    console.log('error_code:' +  data.code + ' msg: ' + data.msg);
                }

            })
            .error(function (data, status, headers, config) {
                console.log('error_code:' + data.code  + ' msg: ' + data.msg);
            })
    };
    
    $scope.computeCV = function () {
        
    };
    
    $scope.computeError = function () {
        
    };
    
    $scope.save = function () {

    };
    
});
