Controller.$inject = ['$scope', '$http'];
function Controller($scope, $http) {
  $scope.login = function() {
    window.location = "../../auth/login";
  };
  $scope.logout = function() {
    window.location = "../../auth/logout";
  };
  $scope.post = function() {
    $http({method: 'POST', url: 'http://192.168.245.154/api/post', data: JSON.stringify({message: $scope.message})}).success(function (data){
      var o = new Object;
      o.id = data.id;
      o.message = $scope.message;
      o.name = $scope.name;
      console.log($scope.posts.datas)
      $scope.posts.datas.splice(0, 0, o)
      console.log($scope.posts.datas)
    });
  };
  $http({method: 'GET', url:'http://192.168.245.154/api/post'}).success(function (data) {
    $scope.posts = data;
  });
  $http({method: 'GET', url:'http://192.168.245.154/auth/status'}).success(function (data){
    $scope.islogin = data.islogin;
    $scope.name = data.username;
    $scope.message = "Type in ..."
  });
};
