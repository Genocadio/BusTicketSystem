const mongoose = require('mongoose');

const busSchema = new mongoose.Schema({
  busNumber: {
    type: String,
    required: true,
    unique: true
  },
  capacity: {
    type: Number,
    required: true
  },
  type: {
    type: String,
    required: true
  },
  operator: {
    type: String,
    required: true
  },
  routes: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Trip'
  }],
  status: {
    type: String,
    enum: ['active', 'inactive', 'maintenance'],
    default: 'active'
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

const Bus = mongoose.model('Bus', busSchema);

module.exports = Bus;
