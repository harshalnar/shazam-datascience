/*
 * User model
 * Most of this is probably not needed, yet the implementation
 * is provided if needed in the future.
 */

var User = require('mongoose').model('User'),
    PythonShell = require('python-shell'),
    passport = require('passport');

var getErrorMessage = function(err) {
  var message = '';

  if (err.code) {
    // Dispensable. Expand if ever needed.
    switch(err.code) {
      // Not really going to happen if we are only having
      //  the root user.
      case 11000:
      case 11001:
        message = 'Username already exists';
        break;
      default:
        message = 'Something went wrong';
    }
  } else {
    for (var errName in err.errors) {
      if (err.errors[errName].message)
        message = err.errors[errName].message;
    }
  }

  return message;
};

exports.getRecommendations = function(req, res) {
  var idString = req.user.idString;

  var options = {
    mode: 'text',
    pythonPath: '/usr/bin/python',
    scriptPath: './scripts',
    args: ['[{"idString": "'+idString+'"}]']
  };

  pyshell = new PythonShell('collaborative_filtering.py', options);

  pyshell.on('message', function(message) {
    console.log(message.split(','));
    console.log(typeof message);
    res.json({'predictions': message.split(',')})
  });

  pyshell.end(function(err) {
    if (err) throw err;
    console.log('Finished');
  })


}

// Middleware that checks if there's a user logged in.
exports.requiresLogin = function(req, res, next) {
  // Here we assume that the ONLY user is the admin,
  // else we could have to a specific authorization middleware.
  // Consider this if project requirements ever change.
  if (!req.isAuthenticated()) {
    return res.status(401).send({
      message: 'You are not logged in as admin'
    });
  }

  next();
};

// Middleware that checks if there's a user logged in.
exports.requiresAdmin= function(req, res, next) {
  // Here we assume that the ONLY user is the admin,
  // else we could have to a specific authorization middleware.
  // Consider this if project requirements ever change.
  if (!req.user.admin) {
    return res.status(403).send({
      message: 'User not authorized'
    });
  }

  next();
};

exports.renderSignin = function(req, res, next) {
  if (!req.user) {
    res.render('signin', {
      title: 'Sign in',
      messages: req.flash('error') || req.flash('info')
    });
  } else {
    return res.redirect('/');
  }
};

exports.renderSignup = function(req, res, next) {
  if (!req.user) {
    res.render('signup', {
      title: "Sign-up form",
      messages: req.flash('error')
    });
  } else {
    return res.redirect('/');
  }
};

// Signin handled by Passport

exports.signup = function(req, res, next) {
  if (!req.user) {
    var user = new User(req.body);
    var message = null;

    user.provider = "local";

    // Create user then log it in.
    user.save(function(err) {
      if (err) {
        var message = getErrorMessage(err);

        req.flash('error', message);
        return res.redirect('/signup');
      }

      req.login(user, function(err) {
        if (err) return next(err);
        return res.redirect('/');
      });
    });
  } else {
    return res.redirect('/');
  }
}

exports.signout = function(req, res) {
  req.logout();
  res.redirect('/');
};

exports.create = function(req, res, next) {
  var user = new User(req.body);
  user.provider = 'local';

  user.save(function(err) {
    if (err) {
      return next(err);
    } else {
      res.json(user);
    }
  });
};

exports.list = function(req, res, next) {
  User.find({}, function(err, users){
    // console.log(users);
    if (err) {
      return next(err);
    } else {
      res.json(users);
    }
  });
};

exports.read = function(req, res) {
  res.json(req.user);
}

exports.update = function(req, res, next) {
  User.findByIdAndUpdate(req.user.id, req.body, function(err, user) {
    if (err) {
      return next(err);
    } else {
      res.json(user);
    }
  });
};

exports.delete = function(req, res, next) {
  req.user.remove(function(err) {
    if (err) {
      return next(err);
    } else {
      res.json(req.user);
    }
  });
};

// Middleware for paths having :userId
exports.userById = function(req, res, next, id) {
  User.findOne({
    _id: id
  }, function(err, user) {
    if (err) {
      return next(err);
    } else {
      req.user= user;
      next();
    }
  });
};
