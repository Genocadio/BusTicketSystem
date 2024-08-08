const express = require('express');
const Booking = require('../models/bookingModel');
const Trip = require('../models/Trip'); // Make sure you have a Trip model
require('dotenv').config();
const mongoose = require('mongoose');

const bookingRouter = express.Router();

// POST /api/bookings - Create a new booking
bookingRouter.post('/', async (req, res, next) => {
    const { tripId, numberOfTickets, totalPrice } = req.body;
    user = req.user
    console.log('extraction : ' + user)
    
    // const userId = req.userId; // Assuming you have middleware to add user ID to req
    const userId = user._id.toString()
    console.log('this is id' + userId)
    if (!tripId || !numberOfTickets || !totalPrice) {
      return res.status(400).json({ error: 'Trip ID, number of tickets, and total price are required' });
    }
  
    try {
      const trip = await Trip.findById(tripId);
      if (!trip) {
        return res.status(404).json({ error: 'Trip not found' });
      }
  
      const newBooking = new Booking({
        tripId,
        userId, // Add user ID to booking
        numberOfTickets,
        totalPrice,
      });
  
      const savedBooking = await newBooking.save();
      res.status(201).json(savedBooking);
    } catch (error) {
      next(error);
    }
  });
// GET /api/bookings/:id - Retrieve a specific booking by ID
bookingRouter.get('/:id', async (req, res, next) => {
  const { id } = req.params;

  try {
    const booking = await Booking.findById(id).populate('tripId');
    if (!booking) {
      return res.status(404).json({ error: 'Booking not found' });
    }

    res.json(booking);
  } catch (error) {
    next(error);
  }
});

// PUT /api/bookings/:id - Update a booking by ID
bookingRouter.put('/:id', async (req, res, next) => {
  const { id } = req.params;
  const { numberOfTickets, totalPrice, status } = req.body;

  try {
    const booking = await Booking.findById(id);
    if (!booking) {
      return res.status(404).json({ error: 'Booking not found' });
    }

    booking.numberOfTickets = numberOfTickets || booking.numberOfTickets;
    booking.totalPrice = totalPrice || booking.totalPrice;
    booking.status = status || booking.status;

    const updatedBooking = await booking.save();
    res.json(updatedBooking);
  } catch (error) {
    next(error);
  }
});

// DELETE /api/bookings/:id - Delete a booking by ID
bookingRouter.delete('/:id', async (req, res, next) => {
  const { id } = req.params;

  try {
    const deletedBooking = await Booking.findByIdAndDelete(id);
    if (!deletedBooking) {
      return res.status(404).json({ error: 'Booking not found' });
    }

    res.status(204).end();
  } catch (error) {
    next(error);
  }
});

bookingRouter.get('/', async (req, res, next) => {
    const user = req.user;
    console.log('User from request:', user);

    // Ensure _id is a valid ObjectId
    if (!user || user === 'undefined' || user === 'null') {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    const userId = user._id.toString();

    // Ensure userId is a valid ObjectId
    if (!mongoose.Types.ObjectId.isValid(userId)) {
        return res.status(400).json({ error: 'Invalid user ID' });
    }

    try {
        // Query bookings using the correct field
        const bookings = await Booking.find({ userId }).populate('tripId');
        
        if (!bookings.length) {
            return res.status(404).json({ error: 'No bookings found for this user' });
        }

        res.json(bookings);
    } catch (error) {
        next(error);
    }
});

module.exports = bookingRouter;
