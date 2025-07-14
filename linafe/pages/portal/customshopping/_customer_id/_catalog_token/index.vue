<template>
  <div>
    <v-row>
      <v-col cols="12" md="12">
        <h1 class="text-center">
          Custom Shopping Cart {{ $route.params.catalog_token }}
        </h1>
        <p class="text-center">
          This is a custom shopping cart page for
          {{ $route.params.customer_id }}.
        </p>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <div v-if="isListView">
          <v-list three-line class="mx-0">
            <ProductListItem
              v-for="item in filteredItems"
              :key="item.id"
              :product="item"
              :show-price="false"
              @click="loadSlideshow"
            />
          </v-list>
        </div>
        <div v-else class="shopping-cart mt-4">
          <ProductCard
            v-for="item in filteredItems"
            :key="item.id"
            :product="item"
            :show-price="false"
            @click="loadSlideshow"
          />
        </div>
      </v-col>
    </v-row>
    <Slideshow
      :data-source="getItemImages"
      :show-slideshow="slideshow"
      @hideSlideshow="slideshow = false"
    />
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import ProductCard from '~/components/shoppingcart/ProductCard.vue'
import ProductListItem from '~/components/shoppingcart/ProductListItem.vue'
import Slideshow from '~/components/shoppingcart/Slideshow'

export default {
  name: 'CustomShopping',
  layout: 'publicapps',

  components: {
    ProductCard,
    ProductListItem,
    Slideshow,
  },

  async asyncData({ params, store, error }) {
    try {
      // await store.dispatch('shoppingcart/products/fetchProducts')
      /* Dejaré comentado este código por si se necesita en un futuro.
      Mientras no se complete la paginación desde el backend, 
      se podría necesitar para pruebas en desarrollo.
      */
      // eslint-disable-next-line camelcase
      const { customer_id, catalog_token } = params
      console.log('Customer ID:', customer_id)
      console.log('Catalog Token:', catalog_token)
      await store.dispatch('shoppingcart/products/fetchData', {
        name: 'Product',
        link: '',
      })
    } catch (err) {
      if (err.response) {
        error({
          statusCode: err.response.status,
          message: err.response.data.message || 'Error fetching products',
        })
      } else {
        error({ statusCode: 500, message: 'Server Error' })
      }
    }
  },
  //   async asyncData({ params }) {
  //     const { customerID, catalogToken } = params
  //     return { customerID, catalogToken }
  //   },

  data: () => ({
    slideshow: false,
    noImgList: [],
  }),

  computed: {
    ...mapGetters('shoppingcart/categories', [
      'getSelectedBrands',
      'isListView',
    ]),

    ...mapGetters('shoppingcart/products', [
      'getAllProducts',
      'getSearchProduct',
      'getItemImages',
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
            (item.name.toLowerCase().includes(searchProduct.toLowerCase()) ||
              item.id.toLowerCase().includes(searchProduct.toLowerCase())) &&
            selectedBrands.includes(item.brand)
          )
        }

        return (
          item.name.toLowerCase().includes(searchProduct.toLowerCase()) ||
          item.id.toLowerCase().includes(searchProduct.toLowerCase())
        )
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

    const customerId = this.$route.params.customer_id
    const token = this.$route.params.catalog_token

    this.setCustomCatalog({
      id: '1',
      token,
      name: 'Custom Shopping',
      link: `/portal/customshopping/${customerId}/${token}`,
      type: 'custom',
      salemanName: 'Demo Salesman',
      salemanEmail: 'demosaleman@numen.pa',
      salemanId: 'demo-salesmanId',
      customerId,
    })

    this.setCustomer({
      id: customerId,
      name: 'Demo Customer',
      email: 'demo@example.com',
    })
  },

  methods: {
    ...mapActions('shoppingcart/products', ['setCountFilteredProducts']),
    ...mapActions('customshopping/customcatalog', [
      'setCustomCatalog',
      'setCustomer',
    ]),
    async loadSlideshow(src) {
      await this.$store.dispatch('shoppingcart/products/fetchItemImages', src)
      this.slideshow = true
    },
  },

  head() {
    return {
      title: 'Shopping Cart',
      meta: [
        {
          hid: 'description',
          name: 'description',
          content: 'A customer shopping cart page for LinaEE Portal.',
        },
      ],
    }
  },
}
</script>
<style lang="scss" scoped>
.shopping-cart {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.product-item {
  margin: 10px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
}
</style>
