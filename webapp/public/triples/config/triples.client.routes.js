angular.module('triples').config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
    when('/triples', {
      templateUrl: 'triples/views/list-triples.client.view.html'
    }).
    when('/triples/create', {
      templateUrl: 'triples/views/create-triple.client.view.html'
    }).
    when('/triples/:tripleId', {
      templateUrl: 'triples/views/view-triple.client.view.html'
    }).
    when('/triples/:tripleId/edit', {
      templateUrl: 'triples/views/edit-triple.client.view.html'
    })
  }
]);
