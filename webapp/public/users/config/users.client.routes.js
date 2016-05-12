angular.module('users').config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
    when('/users', {
      templateUrl: 'users/views/list-users.client.view.html'
    }).
    when('/users/:userId', {
      templateUrl: 'users/views/view-user.client.view.html'
    }).
    when('/suggest/:userId', {
      templateUrl: 'users/views/suggest.client.view.html'
    })
  }
]);
