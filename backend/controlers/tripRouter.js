const express = require('express');
const Trip = require('../models/Trip'); // Ensure the path is correct
require('dotenv').config();

const tripRouter = express.Router();

// POST /api/trips - Create a new trip
tripRouter.post('/', async (req, res, next) => {
  const { bus, location, destination, price, boardingTime } = req.body;

  if (!bus || !location || !destination || !price || !boardingTime) {
    return res.status(400).json({ error: 'Bus, location, destination, price, and boarding time are required' });
  }

  try {
    const newTrip = new Trip({
      bus,
      location,
      destination,
      price,
      boardingTime
    });

    const savedTrip = await newTrip.save();
    res.status(201).json(savedTrip);
  } catch (error) {
    next(error);
  }
});

// GET /api/trips - Retrieve all trips
tripRouter.get('/', async (req, res, next) => {
  try {
    const trips = await Trip.find().populate('bus'); // Populate bus information if needed
    res.json(trips);
  } catch (error) {
    next(error);
  }
});

// GET /api/trips/:id - Retrieve a specific trip by ID
tripRouter.get('/:id', async (req, res, next) => {
  const { id } = req.params;

  try {
    const trip = await Trip.findById(id).populate('bus'); // Populate bus information if needed
    if (!trip) {
      return res.status(404).json({ error: 'Trip not found' });
    }

    res.json(trip);
  } catch (error) {
    next(error);
  }
});

// PUT /api/trips/:id - Update a trip by ID
tripRouter.put('/:id', async (req, res, next) => {
  const { id } = req.params;
  const { bus, location, destination, price, boardingTime } = req.body;

  try {
    const trip = await Trip.findById(id);
    if (!trip) {
      return res.status(404).json({ error: 'Trip not found' });
    }

    trip.bus = bus || trip.bus;
    trip.location = location || trip.location;
    trip.destination = destination || trip.destination;
    trip.price = price || trip.price;
    trip.boardingTime = boardingTime || trip.boardingTime;

    const updatedTrip = await trip.save();
    res.json(updatedTrip);
  } catch (error) {
    next(error);
  }
});

// DELETE /api/trips/:id - Delete a trip by ID
tripRouter.delete('/:id', async (req, res, next) => {
  const { id } = req.params;

  try {
    const deletedTrip = await Trip.findByIdAndDelete(id);
    if (!deletedTrip) {
      return res.status(404).json({ error: 'Trip not found' });
    }

    res.status(204).end();
  } catch (error) {
    next(error);
  }
});

module.exports = tripRouter;
