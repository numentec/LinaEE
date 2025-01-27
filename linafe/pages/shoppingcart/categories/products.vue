<template>
  <div class="shopping-cart mt-4">
    <div v-for="(item, index) in filteredItems" :key="index">
      <ProductCard :product="item" />
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ProductCard from '~/components/shoppingcart/ProductCard.vue'

export default {
  components: {
    ProductCard,
  },

  async asyncData({ store, error }) {
    try {
      // await store.dispatch('shoppingcart/products/fetchProducts')
      /* Dejaré comentado este código por si se necesita en un futuro. 
      Mientras no se complete la paginación desde el backend, 
      se podría necesitar para pruebas en desarrollo.
      */
      await store.dispatch('shoppingcart/products/fetchData', {
        name: 'Product',
        link: '',
      })
    } catch (err) {
      if (err.response) {
        error({
          statusCode: err.response.status,
          message: err.response.data.detail,
        })
      } else {
        error({
          statusCode: 503,
          message: 'No se pudo cargar la lista. Intente luego',
        })
      }
    }
  },

  data() {
    return {}
  },

  computed: {
    ...mapGetters('shoppingcart/categories', ['getSelectedBrands']),

    ...mapGetters('shoppingcart/products', [
      'getAllProducts',
      'getSearchProduct',
    ]),

    filteredItems() {
      return this.getAllProducts.filter((item) => {
        const selectedBrands = this.getSelectedBrands
        let searchProduct = this.getSearchProduct

        if (searchProduct === null || searchProduct === undefined) {
          searchProduct = ''
        }

        if (searchProduct === '' && selectedBrands.length === 0) {
          return true
        }

        if (selectedBrands.length > 0) {
          return (
            item.name.toLowerCase().includes(searchProduct.toLowerCase()) &&
            selectedBrands.includes(item.brand)
          )
        }

        return item.name.toLowerCase().includes(searchProduct.toLowerCase())
      })
    },
  },
  mounted() {
    window.scrollTo(0, 0)
  },
}
</script>

<style scoped>
.shopping-cart {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
</style>
