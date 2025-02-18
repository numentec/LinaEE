<template>
  <div>
    <v-row>
      <v-col cols="12">
        <div v-if="isListView">
          <v-list three-line class="mx-0">
            <ProductListItem
              v-for="item in filteredItems"
              :key="item.id"
              :product="item"
            />
          </v-list>
        </div>
        <div v-else class="shopping-cart mt-4">
          <ProductCard
            v-for="item in filteredItems"
            :key="item.id"
            :product="item"
          />
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import ProductCard from '~/components/shoppingcart/ProductCard.vue'
import ProductListItem from '~/components/shoppingcart/ProductListItem.vue'

export default {
  components: {
    ProductCard,
    ProductListItem,
  },

  async asyncData({ store, error }) {
    try {
      await store.dispatch('shoppingcart/products/fetchProducts')
      /* Dejaré comentado este código por si se necesita en un futuro. 
      Mientras no se complete la paginación desde el backend, 
      se podría necesitar para pruebas en desarrollo.
      */
      // await store.dispatch('shoppingcart/products/fetchData', {
      //   name: 'Product',
      //   link: '',
      // })
    } catch (err) {
      if (err.response) {
        error({
          statusCode: err.response.status,
          message: err.response.data.detail,
        })
      } else {
        error({
          statusCode: 503,
          message: 'Error fetching products',
        })
      }
    }
  },

  data() {
    return {}
  },

  computed: {
    ...mapGetters('shoppingcart/categories', [
      'getSelectedBrands',
      'isListView',
    ]),

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

  watch: {
    filteredItems(newVal) {
      this.setCountFilteredProducts(newVal?.length)
    },
  },

  mounted() {
    window.scrollTo(0, 0)
    this.setCountFilteredProducts(this.filteredItems?.length)
  },

  methods: {
    ...mapActions('shoppingcart/products', ['setCountFilteredProducts']),
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
