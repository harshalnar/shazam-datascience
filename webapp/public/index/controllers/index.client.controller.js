angular.module('index').controller('IndexController', ['$scope',
                                                       'Authentication',
  function($scope, Authentication) {
    $scope.authentication = Authentication;

    $scope.myInterval = 3000;
    $scope.slides= [
      {image: '/img/music1.jpg', title: "Content title 1"},
      {image: '/img/music2.jpg', title: "Content title 2"},
      {image: '/img/music3.jpg', title: "Content title 3"},
      {image: '/img/music4.jpg', title: "Content title 4"},
      {image: '/img/music5.jpg', title: "Content title 5"}
    ];
  }
]);
