export default ({ store }) => {
  store.subscribe((mutation, state) => {
    if (mutation.type.startsWith('shoppingcart/cart/')) {
      localStorage.setItem('lina_cart', JSON.stringify(state.shoppingcart.cart))
    }
  })
}
