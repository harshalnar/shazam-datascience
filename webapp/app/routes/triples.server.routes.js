var users = require('../controllers/users.server.controller'),
    triples = require('../controllers/triples.server.controller');

module.exports = function(app) {
  app.route('/api/triples')
     .get(triples.list)
     .post(triples.create);

  app.route('/api/triples/:tripleId')
     .get(triples.read)
     .put(triples.update)
     .delete(triples.delete);

  // Middleware handling :tripleId
  app.param("tripleId", triples.tripleById);
};
