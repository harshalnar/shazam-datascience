angular.module('triples').factory('Triples', ['$resource',
  function($resource) {
    return $resource('api/triples/:tripleId', {
      tripleId: '@_id'
    }, {
      update: {
        method: 'PUT'
      }
    });
  }
]);
