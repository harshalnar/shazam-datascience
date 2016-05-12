var users = require('../controllers/users.server.controller'),
    songs = require('../controllers/songs.server.controller');

module.exports = function(app) {
  app.route('/api/songs')
     .get(songs.list)
     .post(users.requiresAdmin, songs.create);

  app.route('/api/songs/:songId')
     .get(songs.read)
     .put(users.requiresAdmin, songs.update)
     .delete(users.requiresAdmin, songs.delete);

  // Middleware handling :songId
  app.param("songId", songs.songById);
};
