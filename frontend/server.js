const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const session = require('express-session');
const helmet = require('helmet');
const compression = require('compression');
const morgan = require('morgan');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(helmet({ contentSecurityPolicy: false }));
app.use(compression());
app.use(morgan('combined'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

app.use(session({
  secret: process.env.SESSION_SECRET || 'dev-session-secret-change-in-production',
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    maxAge: 24 * 60 * 60 * 1000
  }
}));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.static(path.join(__dirname, 'public')));

app.use((req, res, next) => {
  res.locals.user = req.session.user || null;
  res.locals.cartCount = req.session.cartCount || 0;
  next();
});

const indexRoutes = require('./routes/index');
const productRoutes = require('./routes/products');
const cartRoutes = require('./routes/cart');
const authRoutes = require('./routes/auth');

app.use('/', indexRoutes);
app.use('/products', productRoutes);
app.use('/electronics', productRoutes);
app.use('/household', productRoutes);
app.use('/books', productRoutes);
app.use('/clothing', productRoutes);
app.use('/sports', productRoutes);
app.use('/bestsellers', productRoutes);
app.use('/giftcards', productRoutes);
app.use('/cart', cartRoutes);
app.use('/auth', authRoutes);

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'healthy', service: 'ecommerce-frontend', timestamp: new Date().toISOString() });
});

app.use((req, res) => {
  res.status(404).render('404', { title: 'Page Not Found', message: 'The page you are looking for does not exist.' });
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).render('error', { title: 'Error', message: 'An unexpected error occurred. Please try again later.' });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Frontend server running on http://0.0.0.0:${PORT}`);
  console.log(`API Backend URL: ${process.env.API_BASE_URL || 'http://localhost:5000'}`);
});

module.exports = app;
