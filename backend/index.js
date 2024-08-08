const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const path = require('path'); // Import path module
const middleware = require('./utils/middleware'); // Import middleware object
 // Example router file, adjust as needed
const logger = require('./utils/logger');
const usersRouter = require('./controlers/userrouter');
const LogiRouter = require('./controlers/Loginrouter');
const busRouter = require('./controlers/busController');
const tripRouter = require('./controlers/tripRouter');
const BookingRouter = require('./controlers/BookingController')
require('dotenv').config();

console.log(process.env.SECRET);

const app = express();

// Apply built-in middlewares
app.use(cors());
app.use(express.json());

// Apply custom middlewares
app.use(middleware.requestLogger);
// app.use(middleware.tokenExtractor);
// app.use(middleware.userExtractor);

// MongoDB connection string
const urI = 'mongodb://localhost:27017/';
const uri = `mongodb+srv://phonebook:Cadio0011@phonebook.qbzboqw.mongodb.net/?retryWrites=true&w=majority&appName=phonebook`;

mongoose.set('strictQuery', false);

logger.info('connecting to: ', uri);

// Connect to MongoDB
mongoose.connect(uri)
  .then(() => {
    logger.info('connected to MongoDB');
  })
  .catch((error) => {
    logger.error('error connecting to MongoDB: ', error.message);
  });

// Serve static files from the 'dist' directory
app.use(express.static(path.join(__dirname, 'dist')));
app.use(middleware.tokenExtractor);

app.use('/api/users', middleware.userExtractor, usersRouter);
app.use('/api/login', LogiRouter);
app.use('/api/buses', middleware.userExtractor, busRouter);
app.use('/api/trips', middleware.userExtractor, tripRouter);
app.use('/api/bookings', middleware.userExtractor, BookingRouter);


// Handle non-API routes by serving index.html
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

// Handle unknown endpoints
app.use(middleware.unkownEndpoint);

// Error handling middleware
app.use(middleware.errorHandler);

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});