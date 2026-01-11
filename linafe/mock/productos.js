// mock/productos.js
export const mockProductos = Array.from({ length: 200 }).map((_, i) => {
  const n = i + 1
  const sku = `SKU-${String(n).padStart(4, '0')}`

  return {
    product_id: `prod_${n}`,
    sku,
    description: `Producto ${n} descripción corta`,
    brand_name: ['Nike', 'Adidas', 'Puma', 'Lina'][i % 4],
    price: Number((5 + (i % 40) * 0.75).toFixed(2)),
    min_qty: (i % 6) + 1,
    max_qty: ((i % 6) + 1) * 12,
    images: [
      {
        url: `https://picsum.photos/300?text=${encodeURIComponent(sku)}`,
        is_primary: true,
      },
    ],
    selected_image_url: `https://picsum.photos/300?text=${encodeURIComponent(
      sku
    )}`,
  }
})
