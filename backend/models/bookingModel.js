// models/Booking.js
const mongoose = require('mongoose');

const bookingSchema = new mongoose.Schema({
  tripId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Trip',
    required: true,
  },
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
  },
  bookingTime: {
    type: Date,
    default: Date.now,
  },
  numberOfTickets: {
    type: Number,
    required: true,
  },
  totalPrice: {
    type: Number,
    required: true,
  },
  status: {
    type: String,
    // enum: ['boarding', 'waiting', 'ended'],
    default: 'waiting',
  },
});

const Booking = mongoose.model('Booking', bookingSchema);

module.exports = Booking;
