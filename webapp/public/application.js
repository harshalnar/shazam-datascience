var mainApplicationModuleName = "pessoa";

var mainApplicationModule = angular.module(mainApplicationModuleName,
                       ['ngResource', 'ngRoute', 'users', 'index', 'songs', 'triples']);

// This makes it indexable by search engine crawlers.
mainApplicationModule.config(['$locationProvider',
  function($locationProvider) {
    $locationProvider.hashPrefix('!');
  }
]);

angular.element(document).ready(function() {
  angular.bootstrap(document, [mainApplicationModuleName]);
});
