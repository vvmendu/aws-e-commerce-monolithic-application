const express = require('express');
const router = express.Router();
const axios = require('axios');
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:5000';

router.get('/', async (req, res) => {
  try {
    const page = req.query.page || 1;
    let category = null;
    const pathSegments = req.originalUrl.split('/').filter(s => s);
    if (pathSegments.length > 0 && pathSegments[0] !== 'products') {
      category = pathSegments[0].split('?')[0];
    }
    const params = {
      page, per_page: 20,
      sort_by: req.query.sort_by || 'created_at',
      sort_order: req.query.sort_order || 'desc'
    };
    if (category) params.category = category;
    if (req.query.min_price) params.min_price = req.query.min_price;
    if (req.query.max_price) params.max_price = req.query.max_price;
    if (req.query.search) params.search = req.query.search;
    const response = await axios.get(`${API_BASE_URL}/api/products`, { params });
    const categoryMap = {
      'electronics': 'Electronics', 'household': 'Household Items',
      'books': 'Books', 'clothing': 'Clothing & Fashion',
      'sports': 'Sports & Outdoors', 'bestsellers': 'Best Sellers', 'giftcards': 'Gift Cards'
    };
    const categoryName = category ? (categoryMap[category] || category) : 'All Products';
    res.render('products', {
      title: categoryName,
      products: response.data.products || [],
      pagination: response.data.pagination || {},
      category, categoryName,
      filters: {
        sort_by: req.query.sort_by || 'created_at',
        sort_order: req.query.sort_order || 'desc',
        min_price: req.query.min_price || '',
        max_price: req.query.max_price || ''
      }
    });
  } catch (error) {
    console.error('Product listing error:', error.message);
    res.render('products', {
      title: 'Products', products: [], pagination: {},
      category: null, categoryName: 'Products', filters: {},
      error: 'Unable to load products. Please try again later.'
    });
  }
});

router.get('/:slug', async (req, res) => {
  try {
    const slug = req.params.slug;
    const response = await axios.get(`${API_BASE_URL}/api/products/slug/${slug}`);
    const product = response.data.product;
    if (!product) {
      return res.status(404).render('404', { title: 'Product Not Found', message: 'The product you are looking for does not exist.' });
    }
    let relatedProducts = [];
    try {
      const relatedRes = await axios.get(`${API_BASE_URL}/api/products`, { params: { category_id: product.category_id, per_page: 4 } });
      relatedProducts = relatedRes.data.products.filter(p => p.id !== product.id).slice(0, 4);
    } catch (err) { console.error('Related products error:', err.message); }
    res.render('product-detail', { title: product.name, product, relatedProducts });
  } catch (error) {
    console.error('Product detail error:', error.message);
    if (error.response && error.response.status === 404) {
      return res.status(404).render('404', { title: 'Product Not Found', message: 'The product you are looking for does not exist.' });
    }
    res.status(500).render('error', { title: 'Error', message: 'Unable to load product details. Please try again later.' });
  }
});

module.exports = router;
