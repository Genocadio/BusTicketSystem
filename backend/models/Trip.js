// models/Trip.js
const mongoose = require('mongoose');

const tripSchema = new mongoose.Schema({
  bus: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Bus', // Reference to the Bus model
    required: true
  },
  location: {
    type: String,
    required: true
  },
  destination: {
    type: String,
    required: true
  },
  price: {
    type: Number,
    required: true
  },
  boardingTime: {
    type: Date,
    required: true
  }
}, { timestamps: true });

const Trip = mongoose.model('Trip', tripSchema);

module.exports = Trip;
