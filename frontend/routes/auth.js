const express = require('express');
const router = express.Router();
const axios = require('axios');
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:5000';

router.get('/login', (req, res) => {
  if (req.session.user) return res.redirect('/');
  res.render('login', { title: 'Login', error: null });
});

router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    if (!email || !password) {
      return res.render('login', { title: 'Login', error: 'Email and password are required' });
    }
    const response = await axios.post(`${API_BASE_URL}/api/users/login`, { email, password });
    req.session.user = response.data.user;
    req.session.token = response.data.token;
    const returnTo = req.query.returnTo || '/';
    res.redirect(returnTo);
  } catch (error) {
    console.error('Login error:', error.message);
    const errorMessage = error.response?.data?.error || 'Login failed. Please try again.';
    res.render('login', { title: 'Login', error: errorMessage });
  }
});

router.get('/register', (req, res) => {
  if (req.session.user) return res.redirect('/');
  res.render('register', { title: 'Register', error: null });
});

router.post('/register', async (req, res) => {
  try {
    const { email, password, confirmPassword, first_name, last_name, phone } = req.body;
    if (!email || !password || !first_name || !last_name) {
      return res.render('register', { title: 'Register', error: 'All required fields must be filled' });
    }
    if (password !== confirmPassword) {
      return res.render('register', { title: 'Register', error: 'Passwords do not match' });
    }
    const response = await axios.post(`${API_BASE_URL}/api/users/register`, { email, password, first_name, last_name, phone });
    req.session.user = response.data.user;
    req.session.token = response.data.token;
    res.redirect('/');
  } catch (error) {
    console.error('Registration error:', error.message);
    const errorMessage = error.response?.data?.error || 'Registration failed. Please try again.';
    res.render('register', { title: 'Register', error: errorMessage });
  }
});

router.get('/logout', (req, res) => {
  req.session.destroy((err) => {
    if (err) console.error('Logout error:', err);
    res.redirect('/');
  });
});

router.get('/profile', async (req, res) => {
  if (!req.session.user) return res.redirect('/auth/login?returnTo=/auth/profile');
  try {
    const response = await axios.get(`${API_BASE_URL}/api/users/profile`, {
      headers: { 'Authorization': `Bearer ${req.session.token}` }
    });
    req.session.user = response.data.user;
    res.render('profile', { title: 'My Profile', user: response.data.user, success: req.query.success, error: null });
  } catch (error) {
    console.error('Profile fetch error:', error.message);
    res.render('profile', { title: 'My Profile', user: req.session.user, success: null, error: 'Unable to load profile data' });
  }
});

module.exports = router;
