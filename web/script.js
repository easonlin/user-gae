Controller.$inject = ['$scope', '$http'];
function Controller($scope, $http) {
  $scope.login = function() {
    window.location = "../../auth/login";
  };
  $scope.logout = function() {
    window.location = "../../auth/logout";
  };
  $scope.post = function() {
    $http({method: 'POST', url: 'http://192.168.245.154/api/post', data: JSON.stringify({message: $scope.message})})
  };
  $http({method: 'GET', url:'http://192.168.245.154/api/post'}).success(function (data) {
    $scope.posts = data;
  });
  $http({method: 'GET', url:'http://192.168.245.154/auth/status'}).success(function (data){
    $scope.islogin = data.islogin;
    $scope.islogin = "true"
    $scope.username = data.username;
    $scope.username = "hi"
  });
};
