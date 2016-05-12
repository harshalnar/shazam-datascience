angular.module('triples').controller('TriplesController',
  ['$scope', '$routeParams', '$location', 'Authentication', 'Triples',
    function($scope, $routeParams, $location, $timeout, $q, $log, Authentication, Triples) {
      $scope.authentication = Authentication;

      $scope.create = function() {
        var triple = new Triples({
          user: this.user,
          song: this.song
        });

        triple.$save(function(response) {
          $location.path('triples/' + response._id);
        }, function(errorResponse) {
          $scope.error = errorResponse.data.message;
        });
      };

      $scope.find = function() {
        $scope.triples= Triples.query();
      };

      $scope.findOne = function() {
        $scope.triple = Triples.get({
          tripleId: $routeParams.tripleId
        });
      };

      $scope.update = function() {
        $scope.triple.$update(function() {
          $location.path('triples/' + $scope.triple._id);
        }, function(errorResponse) {
          $scope.error = errorResponse.data.message;
        });
      };

      $scope.delete = function(triple) {
        if (triple) {
          triple.$remove(function() {
            for (var i in $scope.triples) {
              if ($scope.triples[i] === triple) {
                $scope.triples.splice(i, 1);
              }
            }
          });
        } else {
          $scope.triple.$remove(function() {
            $location.path('triples');
          });
        }
      };
    }
  ]
);
