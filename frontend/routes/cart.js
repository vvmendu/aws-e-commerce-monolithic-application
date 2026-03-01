const express = require('express');
const router = express.Router();
const axios = require('axios');
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:5000';

router.get('/', async (req, res) => {
  if (!req.session.user) return res.redirect('/auth/login?returnTo=/cart');
  try {
    const response = await axios.get(`${API_BASE_URL}/api/cart`, {
      headers: { 'Authorization': `Bearer ${req.session.token}` }
    });
    res.render('cart', {
      title: 'Shopping Cart',
      items: response.data.items || [],
      total: response.data.total || 0,
      count: response.data.count || 0
    });
  } catch (error) {
    console.error('Cart fetch error:', error.message);
    res.render('cart', { title: 'Shopping Cart', items: [], total: 0, count: 0, error: 'Unable to load cart.' });
  }
});

router.post('/add', async (req, res) => {
  if (!req.session.user) return res.status(401).json({ error: 'Login required' });
  try {
    const { product_id, quantity } = req.body;
    await axios.post(`${API_BASE_URL}/api/cart`, { product_id: parseInt(product_id), quantity: parseInt(quantity) || 1 }, {
      headers: { 'Authorization': `Bearer ${req.session.token}` }
    });
    res.json({ success: true, message: 'Item added to cart' });
  } catch (error) {
    const msg = error.response?.data?.error || 'Failed to add item';
    res.status(400).json({ error: msg });
  }
});

router.post('/remove/:itemId', async (req, res) => {
  if (!req.session.user) return res.redirect('/auth/login');
  try {
    await axios.delete(`${API_BASE_URL}/api/cart/${req.params.itemId}`, {
      headers: { 'Authorization': `Bearer ${req.session.token}` }
    });
    res.redirect('/cart');
  } catch (error) {
    console.error('Remove cart error:', error.message);
    res.redirect('/cart');
  }
});

module.exports = router;
