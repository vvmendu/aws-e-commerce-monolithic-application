const express = require('express');
const router = express.Router();
const axios = require('axios');
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:5000';

router.get('/', async (req, res) => {
  try {
    const [featuredRes, bestsellerRes, categoriesRes] = await Promise.all([
      axios.get(`${API_BASE_URL}/api/products/featured?limit=8`),
      axios.get(`${API_BASE_URL}/api/products/bestsellers?limit=8`),
      axios.get(`${API_BASE_URL}/api/categories`)
    ]);
    res.render('index', {
      title: 'ShopNow - Your One-Stop E-Commerce Platform',
      featured: featuredRes.data.products || [],
      bestsellers: bestsellerRes.data.products || [],
      categories: categoriesRes.data.categories || []
    });
  } catch (error) {
    console.error('Homepage error:', error.message);
    res.render('index', {
      title: 'ShopNow - Your One-Stop E-Commerce Platform',
      featured: [], bestsellers: [], categories: [],
      error: 'Unable to load products. Please try again later.'
    });
  }
});

router.get('/search', async (req, res) => {
  try {
    const searchQuery = req.query.q || '';
    const page = req.query.page || 1;
    if (!searchQuery.trim()) return res.redirect('/');
    const response = await axios.get(`${API_BASE_URL}/api/products`, {
      params: { search: searchQuery, page, per_page: 20 }
    });
    res.render('products', {
      title: `Search Results for "${searchQuery}"`,
      products: response.data.products || [],
      pagination: response.data.pagination || {},
      searchQuery, category: null
    });
  } catch (error) {
    console.error('Search error:', error.message);
    res.render('products', {
      title: 'Search Results', products: [], pagination: {},
      searchQuery: req.query.q || '', category: null,
      error: 'Search failed. Please try again.'
    });
  }
});

module.exports = router;
