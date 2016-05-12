// Triple schema.

var mongoose = require('mongoose'),
    Schema = mongoose.Schema;

var TripleSchema = new Schema({
  user: {
    type: Schema.ObjectId,
  },
  song: {
    type: Schema.ObjectId,
  },
  songTitle: {
    type: String,
  },
  songAuthor: {
    type: String,
  },
  count: {
    type: Number,
    default: 1
  }
});

mongoose.model('Triple', TripleSchema);

module.exports = TripleSchema
