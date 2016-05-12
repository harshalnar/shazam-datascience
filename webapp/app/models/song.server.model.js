// Song schema.

var mongoose = require('mongoose'),
    Schema = mongoose.Schema;

var SongSchema = new Schema({
  index: {
    type: Number
  },
  idString: {
    type: String 
  },
  author: {
    type: String,
    required: 'Song must have an author'
  },
  title: {
    type: String,
    required: 'Song must have a title'
  },
});

mongoose.model('Song', SongSchema);

module.exports = SongSchema
