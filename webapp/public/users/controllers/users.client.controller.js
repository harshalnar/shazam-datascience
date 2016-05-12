angular.module('users').controller('UsersController',
  ['$scope', '$routeParams', '$location', '$http', 'Authentication', 'Users', 'Songs',
    function($scope, $routeParams, $location, $http, Authentication, Users, Songs) {
      $scope.authentication = Authentication;

      $scope.suggest = function() {
        userId = $routeParams.userId;
        $http.get('/suggest/' + userId)
        .then(function (res) {
          predictions = res.data.predictions;
          
          $scope.predictions = [];
          angular.forEach(predictions, function(p) {
            Songs.query({'idString': p}, function(res) {
              $scope.predictions.push(res[0]);
            })
          });
        })
      };

      $scope.find = function() {
        $scope.users = Users.query();
      };

      $scope.findOne = function() {
        $scope.user = Users.get({
          userId: $routeParams.userId
        });
      };

      $scope.delete = function(user) {
        if (user) {
          user.$remove(function() {
            for (var i in $scope.users) {
              if ($scope.users[i] === user) {
                $scope.users.splice(i, 1);
              }
            }
          });
        } else {
          $scope.user.$remove(function() {
            $location.path('users');
          });
        }
      };

    }
  ]
);
