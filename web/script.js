JsonController.$inject = ['$scope', '$http'];
function JsonController($scope, $http) {
    $http({method: 'GET', url:'http://192.168.245.154/api/test'}).success(function (data) {
        $scope.user = data;
    });
};
