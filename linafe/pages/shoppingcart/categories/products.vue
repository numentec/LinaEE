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
              @click="loadSlideshow"
            />
          </v-list>
        </div>
        <div v-else class="shopping-cart mt-4">
          <ProductCard
            v-for="item in filteredItems"
            :key="item.id"
            :product="item"
            @click="loadSlideshow"
          />

          <!-- Loading indicator para infinite scroll -->
          <div v-if="isLoadingMore" class="loading-more">
            <v-progress-circular indeterminate color="primary" :size="40" />
            <p class="mt-2">Cargando más productos...</p>
          </div>

          <!-- Mensaje cuando no hay más datos -->
          <div
            v-else-if="allDataLoaded && filteredItems.length > 0"
            class="no-more-data"
          >
            <v-divider class="my-4" />
            <p class="text-center text--secondary">
              Has visto todos los productos disponibles
            </p>
          </div>
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
  components: {
    ProductCard,
    ProductListItem,
    Slideshow,
  },

  async asyncData({ store, error }) {
    store.dispatch(
      'shoppingcart/products/setPageSize',
      process.client && window.innerWidth < 960 ? 25 : 100
    )

    try {
      // Cargar la primera página con resetData=true
      await store.dispatch('shoppingcart/products/fetchProducts', {
        page: 1,
        resetData: true,
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
          message: 'Error fetching products',
        })
      }
    }
  },

  data() {
    return {
      slideshow: false,
      noImgList: [],
      scrollTimeout: null,
    }
  },

  computed: {
    ...mapGetters('shoppingcart/categories', [
      'getSelectedBrands',
      'isListView',
    ]),

    ...mapGetters('shoppingcart/products', [
      'getAllProducts',
      'getSearchProduct',
      'getItemImages',
      'getIsLoadingMore',
      'getAllDataLoaded',
      'getHasNextPage',
    ]),

    isLoadingMore() {
      return this.getIsLoadingMore
    },

    allDataLoaded() {
      return this.getAllDataLoaded
    },

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

    // Agregar event listener para infinite scroll
    window.addEventListener('scroll', this.handleScroll)
    window.addEventListener('resize', this.handleResize)
  },

  beforeDestroy() {
    // Limpiar event listeners
    window.removeEventListener('scroll', this.handleScroll)
    window.removeEventListener('resize', this.handleResize)
  },

  methods: {
    ...mapActions('shoppingcart/products', [
      'setCountFilteredProducts',
      'loadMoreProducts',
    ]),

    async loadSlideshow(src) {
      await this.$store.dispatch('shoppingcart/products/fetchItemImages', src)
      this.slideshow = true
    },

    handleScroll() {
      // Throttle scroll events para mejor performance
      if (this.scrollTimeout) return

      this.scrollTimeout = setTimeout(() => {
        this.checkScrollPosition()
        this.scrollTimeout = null
      }, 100)
    },

    checkScrollPosition() {
      const scrollHeight = document.documentElement.scrollHeight
      const scrollTop = document.documentElement.scrollTop
      const clientHeight = document.documentElement.clientHeight

      // Detectar si estamos cerca del final (200px antes del final)
      const threshold = 200
      const nearBottom = scrollTop + clientHeight >= scrollHeight - threshold

      if (nearBottom && this.shouldLoadMore()) {
        this.loadMore()
      }
    },

    shouldLoadMore() {
      return (
        this.getHasNextPage &&
        !this.isLoadingMore &&
        !this.allDataLoaded &&
        this.filteredItems.length > 0
      )
    },

    async loadMore() {
      try {
        await this.loadMoreProducts()
      } catch (error) {
        // Manejo silencioso del error para mejor UX
        // El usuario no verá errores durante el scroll
      }
    },

    handleResize() {
      // Recalcular si necesitamos cargar más datos cuando cambia el tamaño
      this.$nextTick(() => {
        this.checkScrollPosition()
      })
    },

    isMobile() {
      return this.$vuetify.breakpoint.mobile
    },
  },
}
</script>

<style scoped>
.shopping-cart {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.loading-more {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  text-align: center;
}

.loading-more p {
  margin-top: 1rem;
  color: #666;
  font-size: 0.9rem;
}

.no-more-data {
  width: 100%;
  padding: 2rem 1rem;
  text-align: center;
}

.no-more-data p {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.7;
}

/* Smooth transitions */
.loading-more,
.no-more-data {
  opacity: 0;
  animation: fadeIn 0.3s ease forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .loading-more,
  .no-more-data {
    padding: 1.5rem 0.5rem;
  }
}
</style>
