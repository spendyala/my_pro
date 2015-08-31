function UserController($scope, $http) {
  $http.defaults.xsrfCookieName = 'csrftoken';
  $http.defaults.xsrfHeaderName = 'X-CSRFToken';
  $http.defaults.withCredentials = true;

    $scope.user = {};
    $scope.createUser = function() {
        $http({
            method : 'POST',
            url : '/vfd_app/test',
            data : 'name=' + $scope.user.name + '&email=' + $scope.user.email,
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        })
    }
}

angular.module('submitmodule', ['datatables'])
.controller('UserController', UserController).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
