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
      const items = await store.dispatch('shoppingcart/categories/fetchData', {
        name: 'Product',
        link: '',
      })

      return items
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
    return {
      items: [],
    }
  },

  computed: {
    ...mapGetters('shoppingcart/categories', [
      'getSelectedBrands',
      'getSearchProduct',
    ]),

    filteredItems() {
      return this.items.filter((item) => {
        const selectedBrands = this.getSelectedBrands
        let SearchProduct = this.getSearchProduct

        if (SearchProduct === null || SearchProduct === undefined) {
          SearchProduct = ''
        }

        if (SearchProduct === '' && selectedBrands.length === 0) {
          return true
        }

        if (selectedBrands.length > 0) {
          return (
            item.name.toLowerCase().includes(SearchProduct.toLowerCase()) &&
            selectedBrands.includes(item.brands[0])
          )
        }

        return item.name.toLowerCase().includes(SearchProduct.toLowerCase())
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
