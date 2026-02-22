// mock/productos.js
export const mockProductos = Array.from({ length: 200 }).map((_, i) => {
  const n = i + 1
  const sku = `SKU-${String(n).padStart(4, '0')}`

  const imageCount = Math.floor(Math.random() * 3) + 2
  const images = Array.from({ length: imageCount }).map((_, j) => {
    if (j === 0) {
      return {
        url: `https://picsum.photos/seed/${encodeURIComponent(sku)}/300`,
        is_primary: true,
      }
    } else {
      return {
        url: `https://picsum.photos/seed/${encodeURIComponent(sku)}+${j}/300`,
        is_primary: false,
      }
    }
  })

  return {
    product_id: `prod_${n}`,
    sku,
    description: `Producto ${n} descripción corta`,
    brand_name: ['Nike', 'Adidas', 'Puma', 'Lina'][i % 4],
    price: Number((5 + (i % 40) * 0.75).toFixed(2)),
    min_qty: (i % 6) + 1,
    max_qty: ((i % 6) + 1) * 12,
    images,
    selected_image_url: images[0].url,
  }
})
