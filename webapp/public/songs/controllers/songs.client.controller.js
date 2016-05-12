angular.module('songs').controller('SongsController',
  ['$scope', '$routeParams', '$location', '$timeout', '$q', '$log', 'Authentication', 'Songs', 'Triples',
    function($scope, $routeParams, $location, $timeout, $q, $log, Authentication, Songs, Triples) {
      var self = this;
      $scope.authentication = Authentication;

      self.simulateQuery = false;
      self.isDisabled    = false;
      self.repos         = []//loadAll();
      self.querySearch   = querySearch;
      self.selectedItemChange = selectedItemChange;
      self.searchTextChange   = searchTextChange;

      function findTriple(triple) {
        for (var i = 0; i<$scope.triples.length; i++) {
          if ($scope.triples[i]._id == triple._id) {
            $scope.triples.splice(i, 1);
          }
        }
        $scope.triples.unshift(triple);
      }

      $scope.submit = function(selectedSong) {
        if (!Authentication.user) {
          $location.path('/');
          return;
        }
        if (!selectedSong) {
          return;
        }
  
        existsQuery = {
          user: Authentication.user._id,
          song: selectedSong._id
        };

        Triples.query(existsQuery, function(res) {
          //console.log(res);

          // New song from user, create
          if (res.length == 0) {
            newParams = existsQuery;
            newParams.songTitle = selectedSong.title;
            newParams.count = 1;

            var triple = new Triples(newParams)

            triple.$save(function(response) {
              $scope.triples.unshift(response);
              //$location.path('/triples' + response._id);
            }, function(errorResponse) {
              $scope.error = errorResponse.data.message;
              console.log(errorResponse.data.message)
            });
          } else if (res.length == 1){ // Existing song
            res[0].count = res[0].count + 1;
            res[0].$update(function(ress) {
              findTriple(ress);
            });

          } else {
            console.log('Should never arrive here!!!!!');
          }

          self.selectedItem = undefined;
          $('#input-0').val('');

        });

      }

      $scope.create = function() {
        var song = new Songs({
          index: this.index,
          author: this.author,
          title: this.title
        });

        song.$save(function(response) {
          $location.path('songs/' + response._id);
        }, function(errorResponse) {
          $scope.error = errorResponse.data.message;
        });
      };

      $scope.find = function() {
        if (!Authentication.user) {
          $location.path('/');
          return;
        }
        //console.log($location.search());
        $scope.songs = Songs.query($location.search(), function(res) {
          self.repos = loadAll();
        });
        $scope.triples = Triples.query({user: Authentication.user._id});
      };

      $scope.findOne = function() {
        $scope.song = Songs.get({
          songId: $routeParams.songId
        });
      };

      $scope.update = function() {
        $scope.song.$update(function() {
          $location.path('songs/' + $scope.song._id);
        }, function(errorResponse) {
          $scope.error = errorResponse.data.message;
        });
      };

      $scope.delete = function(song) {
        if (song) {
          song.$remove(function() {
            for (var i in $scope.songs) {
              if ($scope.songs[i] === song) {
                $scope.songs.splice(i, 1);
              }
            }
          });
        } else {
          $scope.song.$remove(function() {
            $location.path('songs');
          });
        }
      };

      // ******************************
      // Internal methods
      // ******************************
      /**
      * Search for repos... use $timeout to simulate
      * remote dataservice call.
      */
      function querySearch (query) {
        // console.log($scope.songs)
        var results = query ? $scope.songs.filter( createFilterFor(query) ) : $scope.songs,//$scope.songs
            deferred;
        if (self.simulateQuery) {
          deferred = $q.defer();
          $timeout(function () { deferred.resolve( results ); }, Math.random() * 1000, false);
          return deferred.promise;
        } else {
          return results;
        }
      }
      function searchTextChange(text) {
        $log.info('Text changed to ' + text);
      }
      function selectedItemChange(item) {
        $log.info('Item changed to ' + JSON.stringify(item));
        $scope.submit(item);
      }
      /**
      * Build `components` list of key/value pairs
      * TODO: Load with actual data.
      */
      function loadAll() {
        /*var songs = [
          {
            '_id'       : "1",
            'name'      : 'Oasis',
            'artist'    : 'Wonderwall',
            'album'     : 'Album',
          },
          {
            '_id'       : "2",
            'name'      : 'Snoop Dog',
            'artist'    : 'Weed',
            'album'     : 'Album',
          },
          {
            '_id'       : "3",
            'name'      : 'Metallica',
            'artist'    : 'Enter Sand Man',
            'album'     : 'Album',
          },
          {
            '_id'       : "4",
            'name'      : 'Foster the People',
            'artist'    : 'Wooohooo',
            'album'     : 'Foster',
          },
          {
            '_id'       : "5",
            'name'      : 'Dream Theater',
            'artist'    : 'Dance of Etentiy',
            'album'     : 'Scenes from a Memory',
          }
        ];*/
        return $scope.songs.map( function (repo) {
          repo.value = repo.title.toLowerCase();
          return repo;
        });
      }
      /**
      * Create filter function for a query string
      */
      function createFilterFor(query) {
        var lowercaseQuery = angular.lowercase(query);
        return function filterFn(item) {
          return (item.value.indexOf(lowercaseQuery) === 0);
        };
      }
    }
  ]
);
