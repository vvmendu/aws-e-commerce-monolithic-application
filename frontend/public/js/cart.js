function addToCart(productId, quantity = 1) {
  fetch('/cart/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id: productId, quantity: quantity })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      showToast('Item added to cart!', 'success');
    } else {
      showToast(data.error || 'Failed to add item', 'danger');
    }
  })
  .catch(err => showToast('Error adding to cart', 'danger'));
}

function showToast(message, type = 'success') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = `toast align-items-center text-white bg-${type} border-0 show`;
  toast.setAttribute('role', 'alert');
  toast.innerHTML = `<div class="d-flex"><div class="toast-body">${message}</div><button type="button" class="btn-close btn-close-white me-2 m-auto" onclick="this.closest('.toast').remove()"></button></div>`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}
