/**
 * Created by hzhehui on 3/9/2016.
 */
var app = angular.module('Hello', ['ui.router']);

app.config(['$stateProvider', '$urlRouterProvider', '$httpProvider', function ($stateProvider, $urlRouterProvider, $httpProvider) {

    $httpProvider.defaults.headers.post['Content-Type'] = 'text/plain';

    $stateProvider.state('main', {
        url:'/',
        templateUrl:'/static/main.html'
    })

        .state('curve', {
            url:'/curve',
            templateUrl:'/static/curve_result.html'
        });

    $urlRouterProvider
        .otherwise('/');
}]);
