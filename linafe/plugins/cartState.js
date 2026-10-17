export default ({ store }) => {
  store.subscribe((mutation, state) => {
    if (mutation.type.startsWith('saleapp/cart/')) {
      localStorage.setItem('lina_cart', JSON.stringify(state.saleapp.cart))
    }
  })
}
