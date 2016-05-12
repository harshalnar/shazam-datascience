var seeder = require('mongoose-seed');
var userData = require('./seeds/User.json');
var songData = require('./seeds/Song.json');
var tripleData = require('./seeds/Triple.json');
 
// Connect to MongoDB via Mongoose 
seeder.connect('mongodb://localhost/songgest', function() {
  
  // Load Mongoose models 
  seeder.loadModels([
    'app/models/user.server.model.js',
    'app/models/song.server.model.js',
    'app/models/triple.server.model.js',
  ]);
 
  // Clear specified collections 
  seeder.clearModels(['User', 'Song', 'Triple'], function() {
 
    // Callback to populate DB once collections have been cleared 
    console.log(userData[0].documents[0]);
    console.log(songData[0].documents[0]);
    console.log(tripleData[0].documents[0]);
    seeder.populateModels(userData);
    seeder.populateModels(songData);
    seeder.populateModels(tripleData);
 
  });
});
