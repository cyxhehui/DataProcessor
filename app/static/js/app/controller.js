/**
 * Created by hzhehui on 3/9/2016.
 */
//var app = angular.module('Hello', []);
app.controller('cvCtrl', ['$scope', '$http', 'DataService', function($scope, $http, dataService){
    $scope.cvResults = [];

    dataService.computeCV();

    dataService.registerListener('cvCtrl', 'eventComputeCVFinished', function () {
        $scope.cvResults = dataService.getCvResults();
    });


    $scope.$on('$destroy', function () {
       dataService.unregisterListener(cvCtrl);
    });
    /***************init code***************/
    $scope.cvResults = dataService.getCvResults();
}]);

app.controller('curveCtrl', function ($scope, $http) {

    $scope.showImage = false;

    console.log($scope.$parent);
    var request = $http({
        method:'GET',
        url:'api/curve_fit',
        params:{'isall':true}
    });

    $scope.showImage = true;
    $scope.imgSrc = "static/images/logistic.png";
    var htmlstr = "";
    request.success(function (data, status, headers, config) {
            if(data.code == 1) {
                    $scope.showImage = true;
                    $scope.imageSrc = "static/images/logistic.png";
                }
                else if(data.code == 0){
                    console.log('error_code:' +  data.code + ' msg: ' + data.msg);
                    htmlstr = "<tr><td></td><td></td><td>拟合失败,无可用曲线图</td></tr>";
                }
        })
        .error(function (data, status, headers, config) {

        });

});

app.controller('helloCtrl', ['$scope', '$http', 'DataService', function($scope, $http, dataService){

    $scope.dataSources = ['NE', 'DA'];
    $scope.selectedDataSource = 'DA';
    $scope.isComputedError = false;
    $scope.isSelectAll = false;
    $scope.isComputeErrorAll = false;

    $scope.changeDataSource = function () {
        $scope.selectedDataSource = this.selectedDataSource;
        console.log("select source:" + $scope.selectedDataSource);
    };

    $scope.hasData = function () {
        if($scope.dataItems)
            return true;
        else
            return false;
    };

    $scope.selectAll = function (isSelectall) {
        if($scope.dataItems){

            if(isSelectall){
                console.log("ts");
                for(var i = 0; i < $scope.dataItems.length; i++){
                    $scope.dataItems[i].isSelectedForCurve = true;
                }
            }
            else{
                console.log("ts1");
                for(var i = 0; i < $scope.dataItems.length; i++){
                    $scope.dataItems[i].isSelectedForCurve = false;
                }
            }
        }
    };

    $scope.computeErrAllCheckOrUncheck = function (isComputeErrorAll) {

        if($scope.dataItems){

            if(isComputeErrorAll){
                for(var i = 0; i < $scope.dataItems.length; i++){
                    $scope.dataItems[i].isSelectedForCompErr = true;
                }
            }
            else{
                console.log("ts1");
                for(var i = 0; i < $scope.dataItems.length; i++){
                    $scope.dataItems[i].isSelectedForCompErr = false;
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

        dataService.dataLoad($scope.selectedDataSource);
    };

    $scope.loadRealx = function () {

        dataService.loadRealx();
    };

    $scope.curveFit = function () {
        console.log('curve fit');
        var selected_array = [];
        var i = 0;
        for(i = 0; i < $scope.dataItems.length; i++){
            if($scope.dataItems[i].isSelectedForCurve){
                selected_array.push(i);
            }
        }
        //console.log(selected_array);
        //console.log(angular.fromJson($scope.dataItems));

        if(selected_array.length == 0){

            //error: alter
            console.log("please choose data to curve");
        }

        var request = $http({
            method:'GET',
            url:'show_curve_result.html',
            params:{'selecteditems': angular.toJson(selected_array)}
        });

        var htmlstr = "";
        request.success(function (data, status, headers, config) {
                console.log('status:' + status + 'msg: ' + data.msg);
                if(data.code == 1) {
                    htmlstr = "<img src=\"{% static 'images/logistic.png' %}\"  alt=\"拟合结果\" />"
                }
                else if(data.code == 0){
                    console.log('error_code:' +  data.code + ' msg: ' + data.msg);
                    htmlstr = "<tr><td></td><td></td><td>拟合失败,无可用曲线图</td></tr>";
                }

            })
            .error(function (data, status, headers, config) {
                console.log('error_code:' + data.code  + ' msg: ' + data.msg);
            })

         $("#image-content").html(htmlstr);
    };

    $scope.computeCV = function () {

    };

    $scope.computeError = function (id) {
        $scope.dataItems[id - 1]['hasComputed'] = true;
        dataService.computeError(id);
    };

    $scope.computeMultipleXError = function () {
        var computeErrorArray = []
        for (var i = 0 ; i < $scope.dataItems.length; i++){
            if($scope.dataItems[i]['isSelectedForCompErr'])
                computeErrorArray.push($scope.dataItems[i]['id']);
        }
        dataService.computeMultipleXError(computeErrorArray);
    };

    $scope.save = function () {

    };

    /*************listener for events****************/
    dataService.registerListener('helloCtrl', 'eventDataLoadFinished', function () {
        $scope.dataItems = dataService.getDataItems();
    });

    dataService.registerListener('helloCtrl', 'eventRealxLoadFinished', function () {
        $scope.dataItems = dataService.getDataItems();
    });

    dataService.registerListener('helloCtrl', 'eventComputeMultipleErrorFinished', function () {
        $scope.dataItems = dataService.getDataItems();
    });


    $scope.$on('$destroy', function () {
       dataService.unregisterListener(helloCtrl);
    });
    /***************init code***************/
    $scope.dataItems = dataService.getDataItems();
}]);
