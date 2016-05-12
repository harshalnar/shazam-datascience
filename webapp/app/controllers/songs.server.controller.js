var Song = require('mongoose').model('Song');

var getErrorMessage = function(err) {
  if (err.errors) {
    for (var errName in err.errors) {
      if (err.errors[errName].message)
        return err.errors[errName].message;
    }
  } else {
    return 'Unknown server error';
  }
};

exports.create = function(req, res, next) {
  var song = new Song(req.body);

  song.save(function(err) {
    if (err) {
      return res.status(400).send({
        message: getErrorMessage(err)
      });
    } else {
      res.json(song);
    }
  });
};

exports.list = function(req, res, next) {
  Song.find(req.query, function(err, songs){
    if (err) {
      return res.status(400).send({
        message: getErrorMessage(err)
      });
    } else {
      res.json(songs);
    }
  });
};

exports.read = function(req, res) {
  res.json(req.song);
}

exports.update = function(req, res, next) {
  Song.findByIdAndUpdate(req.song.id, req.body, function(err, song) {
    if (err) {
      return res.status(400).send({
        message: getErrorMessage(err)
      });
    } else {
      res.json(song);
    }
  });
};

exports.delete = function(req, res, next) {
  req.song.remove(function(err) {
    if (err) {
      return res.status(400).send({
        message: getErrorMessage(err)
      });
    } else {
      res.json(req.song);
    }
  });
};

// Middleware for paths having :songId
exports.songById = function(req, res, next, id) {
  Song.findOne({
    _id: id
  }, function(err, song) {
    if (err) return next(err);
    if (!song) {
      return next(new Error('Failed to load song ' + id));
    }
    req.song = song;
    next();
  });
};
