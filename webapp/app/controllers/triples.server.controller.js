var Triple = require('mongoose').model('Triple');

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
  var triple = new Triple(req.body);

  triple.save(function(err) {
    if (err) {
      return res.status(400).send({
        message: getErrorMessage(err)
      });
    } else {
      res.json(triple);
    }
  });
};

exports.list = function(req, res, next) {
  Triple.find(req.query, function(err, triples){
    if (err) {
      return res.status(400).send({
        message: getErrorMessage(err)
      });
    } else {
      res.json(triples)//.map(function(elem){
        //elem.populate('user', 'username').populate('song', 'title')
      //}));
    }
  });
};

exports.read = function(req, res) {
  res.json(req.triple);
}

exports.update = function(req, res, next) {
  Triple.findByIdAndUpdate(req.triple.id, req.body, function(err, triple) {
    if (err) {
      return res.status(400).send({
        message: getErrorMessage(err)
      });
    } else {
      res.json(req.body);
    }
  });
};

exports.delete = function(req, res, next) {
  req.triple.remove(function(err) {
    if (err) {
      return res.status(400).send({
        message: getErrorMessage(err)
      });
    } else {
      res.json(req.triple);
    }
  });
};

// Middleware for paths having :songId
exports.tripleById = function(req, res, next, id) {
  Triple.findOne({
    _id: id
  }, function(err, triple) {
    if (err) return next(err);
    if (!triple) {
      return next(new Error('Failed to load triple ' + id));
    }
    req.triple = triple;
    next();
  });
};
