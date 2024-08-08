const express = require('express');
const Bus = require('../models/busModel');
require('dotenv').config();

const busRouter = express.Router();

// POST /api/buses - Create a new bus
busRouter.post('/', async (req, res, next) => {
  const { busNumber, capacity, type, operator, routes } = req.body;

  if (!busNumber || !capacity || !type || !operator) {
    return res.status(400).json({ error: 'Bus number, capacity, type, and operator are required' });
  }

  try {
    const newBus = new Bus({
      busNumber,
      capacity,
      type,
      operator,
      routes
    });

    const savedBus = await newBus.save();
    res.status(201).json(savedBus);
  } catch (error) {
    next(error);
  }
});

// GET /api/buses - Retrieve all buses
busRouter.get('/', async (req, res, next) => {
  try {
    const buses = await Bus.find().populate('routes');
    res.json(buses);
  } catch (error) {
    next(error);
  }
});

// GET /api/buses/:id - Retrieve a specific bus by ID
busRouter.get('/:id', async (req, res, next) => {
  const { id } = req.params;

  try {
    const bus = await Bus.findById(id).populate('routes');
    if (!bus) {
      return res.status(404).json({ error: 'Bus not found' });
    }

    res.json(bus);
  } catch (error) {
    next(error);
  }
});

// PUT /api/buses/:id - Update a bus by ID
busRouter.put('/:id', async (req, res, next) => {
  const { id } = req.params;
  const { busNumber, capacity, type, operator, routes, status } = req.body;

  try {
    const bus = await Bus.findById(id);
    if (!bus) {
      return res.status(404).json({ error: 'Bus not found' });
    }

    bus.busNumber = busNumber || bus.busNumber;
    bus.capacity = capacity || bus.capacity;
    bus.type = type || bus.type;
    bus.operator = operator || bus.operator;
    bus.routes = routes || bus.routes;
    bus.status = status !== undefined ? status : bus.status;

    const updatedBus = await bus.save();
    res.json(updatedBus);
  } catch (error) {
    next(error);
  }
});

// DELETE /api/buses/:id - Delete a bus by ID
busRouter.delete('/:id', async (req, res, next) => {
  const { id } = req.params;

  try {
    const deletedBus = await Bus.findByIdAndDelete(id);
    if (!deletedBus) {
      return res.status(404).json({ error: 'Bus not found' });
    }

    res.status(204).end();
  } catch (error) {
    next(error);
  }
});

module.exports = busRouter;
