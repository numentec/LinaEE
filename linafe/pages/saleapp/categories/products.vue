<template>
  <div>
    <div class="stock-filter-toolbar">
      <v-btn v-show="false" outlined color="primary" @click="openStockFilters">
        <v-icon left>mdi-tune-variant</v-icon>
        Filter stock
        <v-chip v-if="activeStockFilterCount" x-small class="ml-2">
          {{ activeStockFilterCount }}
        </v-chip>
      </v-btn>
    </div>
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
    <v-bottom-sheet v-model="stockFiltersOpen" inset>
      <v-sheet class="stock-filter-sheet mx-auto">
        <div class="stock-filter-heading">
          <h2>Filters</h2>
          <v-btn icon aria-label="Close filters" @click="closeStockFilters">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>
        <v-alert v-if="stockFilterError" dense type="error">
          {{ stockFilterError }}
        </v-alert>
        <v-row dense align="center" class="stock-filter-row">
          <v-col cols="12">
            <v-autocomplete
              v-model="stockFilterDraft.descrips"
              :items="descripOptions"
              :search-input.sync="descripSearch"
              :loading="descripLoading"
              :no-data-text="descripNoDataText"
              :menu-props="descripMenuProps"
              item-text="name"
              item-value="name"
              label="Description"
              placeholder="Type to search descriptions"
              autocomplete="off"
              multiple
              no-filter
              clearable
              dense
              :hint="descripHint"
              persistent-hint
              :hide-details="!descripHint"
            >
              <template v-slot:selection="{ item, index }">
                <v-chip
                  v-if="index < descripVisibleChips"
                  small
                  close
                  @click:close="removeDescrip(item.name)"
                >
                  <span class="descrip-chip-text">{{ item.name }}</span>
                </v-chip>
                <span
                  v-if="index === descripVisibleChips"
                  class="grey--text text-caption"
                >
                  (+{{ stockFilterDraft.descrips.length - descripVisibleChips }}
                  more)
                </span>
              </template>
              <template v-slot:item="{ item, attrs, on }">
                <v-list-item v-bind="attrs" v-on="on">
                  <template v-slot:default="{ active }">
                    <v-list-item-action class="mr-3">
                      <v-checkbox
                        :input-value="active"
                        dense
                        hide-details
                        readonly
                      />
                    </v-list-item-action>
                    <v-list-item-content>
                      <v-list-item-title>{{ item.name }}</v-list-item-title>
                      <v-list-item-subtitle v-if="item.products">
                        {{ item.products }}
                        {{ item.products === 1 ? 'product' : 'products' }}
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </template>
                </v-list-item>
              </template>
            </v-autocomplete>
          </v-col>
        </v-row>
        <v-row dense align="center" class="stock-filter-row">
          <v-col cols="12">
            <v-text-field
              v-model="stockFilterDraft.skuPrefix"
              label="SKU starts with"
              placeholder="Enter the beginning of a SKU"
              maxlength="50"
              clearable
              dense
              hide-details
              @keyup.enter="applyStockFilters"
            />
          </v-col>
        </v-row>
        <v-row
          v-for="textFilter in textFilterFields"
          :key="textFilter.field"
          dense
          align="center"
          class="stock-filter-row"
        >
          <v-col cols="12">
            <v-text-field
              v-model="stockFilterDraft[textFilter.field]"
              :label="textFilter.label"
              maxlength="50"
              clearable
              dense
              hide-details
              @keyup.enter="applyStockFilters"
            />
          </v-col>
        </v-row>
        <v-row
          v-for="metric in stockFilterMetrics"
          :key="metric.field"
          dense
          align="center"
          class="stock-filter-row"
        >
          <v-col cols="1">
            <small>{{ metric.label }}</small>
          </v-col>
          <v-col cols="3">
            <v-select
              v-model="stockFilterDraft[metric.field].operator"
              :items="stockFilterOperators"
              item-text="symbol"
              item-value="value"
              label="Condition"
              clearable
              dense
              hide-details
            >
              <template v-slot:item="{ item, attrs, on }">
                <v-list-item v-bind="attrs" v-on="on">
                  <v-list-item-content>
                    <v-icon v-text="item.icon"></v-icon>
                  </v-list-item-content>
                </v-list-item>
              </template>
              <template v-slot:selection="{ item }">
                <span
                  class="operator-symbol"
                  :aria-label="item.label"
                  :title="item.label"
                >
                  {{ item.symbol }}
                </span>
              </template>
            </v-select>
          </v-col>
          <v-col
            v-if="stockFilterDraft[metric.field].operator"
            :cols="
              stockFilterDraft[metric.field].operator === 'between' ? 4 : 8
            "
          >
            <v-text-field
              v-model.number="stockFilterDraft[metric.field].value"
              :label="
                stockFilterDraft[metric.field].operator === 'between'
                  ? 'From'
                  : 'Quantity'
              "
              type="number"
              step="1"
              inputmode="numeric"
              dense
              hide-details
            />
          </v-col>
          <v-col
            v-if="stockFilterDraft[metric.field].operator === 'between'"
            cols="4"
          >
            <v-text-field
              v-model.number="stockFilterDraft[metric.field].valueTo"
              label="To"
              type="number"
              step="1"
              inputmode="numeric"
              dense
              hide-details
            />
          </v-col>
        </v-row>
        <v-divider class="my-3" />
        <div class="stock-filter-actions">
          <v-btn text :disabled="isLoading" @click="clearStockFilters">
            Clear
          </v-btn>
          <v-spacer />
          <v-btn
            color="primary"
            :loading="isLoading"
            @click="applyStockFilters"
          >
            Apply
          </v-btn>
        </div>
      </v-sheet>
    </v-bottom-sheet>
    <v-fab-transition>
      <v-btn
        v-if="showBackToTop"
        class="back-to-top"
        color="primary"
        fab
        small
        fixed
        bottom
        right
        dark
        aria-label="Back to top"
        title="Back to top"
        @click="scrollToTop"
      >
        <v-icon>mdi-chevron-double-up</v-icon>
      </v-btn>
    </v-fab-transition>
    <Slideshow
      :data-source="getItemImages"
      :show-slideshow="slideshow"
      @hideSlideshow="slideshow = false"
    />
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import ProductCard from '~/components/saleapp/ProductCard.vue'
import ProductListItem from '~/components/saleapp/ProductListItem.vue'
import Slideshow from '~/components/saleapp/Slideshow'

const STOCK_FILTER_METRICS = [
  { field: 'instock', label: 'Now' },
  { field: 'intransit', label: 'Tran' },
  { field: 'infuture', label: 'Fut' },
]

const TEXT_FILTER_FIELDS = [
  { field: 'color', label: 'Color' },
  { field: 'acabado', label: 'Acabado' },
]

const STOCK_FILTER_OPERATORS = [
  { symbol: '=', label: 'Igual a', value: 'eq', icon: 'mdi-equal' },
  {
    symbol: '≠',
    label: 'Distinto de',
    value: 'ne',
    icon: 'mdi-not-equal-variant',
  },
  { symbol: '>', label: 'Mayor que', value: 'gt', icon: 'mdi-greater-than' },
  {
    symbol: '≥',
    label: 'Mayor o igual',
    value: 'gte',
    icon: 'mdi-greater-than-or-equal',
  },
  { symbol: '<', label: 'Menor que', value: 'lt', icon: 'mdi-less-than' },
  {
    symbol: '≤',
    label: 'Menor o igual',
    value: 'lte',
    icon: 'mdi-less-than-or-equal',
  },
  {
    symbol: '↔',
    label: 'Entre (rango)',
    value: 'between',
    icon: 'mdi-arrow-left-right',
  },
]
const BACK_TO_TOP_THRESHOLD = 400
const DESCRIP_SEARCH_MIN_LENGTH = 2
const DESCRIP_SEARCH_DELAY = 300
const MAX_DESCRIP_FILTERS = 30
const DESCRIP_TEXT_MAX_LENGTH = 50

function emptyStockFilters() {
  const filters = STOCK_FILTER_METRICS.reduce((filters, metric) => {
    filters[metric.field] = { operator: '', value: '', valueTo: '' }
    return filters
  }, {})

  TEXT_FILTER_FIELDS.forEach((textFilter) => {
    filters[textFilter.field] = ''
  })

  filters.descrips = []
  filters.skuPrefix = ''

  return filters
}

function cloneStockFilters(filters) {
  const copy = STOCK_FILTER_METRICS.reduce((copy, metric) => {
    const criterion = (filters && filters[metric.field]) || {}
    copy[metric.field] = {
      operator: criterion.operator || '',
      value:
        criterion.value === undefined || criterion.value === null
          ? ''
          : criterion.value,
      valueTo:
        criterion.valueTo === undefined || criterion.valueTo === null
          ? ''
          : criterion.valueTo,
    }
    return copy
  }, {})

  TEXT_FILTER_FIELDS.forEach((textFilter) => {
    copy[textFilter.field] = (filters && filters[textFilter.field]) || ''
  })

  copy.descrips = [...((filters && filters.descrips) || [])]
  copy.skuPrefix = (filters && filters.skuPrefix) || ''

  return copy
}

export default {
  components: {
    ProductCard,
    ProductListItem,
    Slideshow,
  },

  async asyncData({ store, error }) {
    store.dispatch(
      'saleapp/products/setPageSize',
      process.client && window.innerWidth < 960 ? 25 : 100
    )

    try {
      // Cargar la primera página con resetData=true
      await store.dispatch('saleapp/products/fetchProducts', {
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
      stockFiltersOpen: false,
      stockFilterDraft: emptyStockFilters(),
      stockFilterError: '',
      stockFilterMetrics: STOCK_FILTER_METRICS,
      textFilterFields: TEXT_FILTER_FIELDS,
      stockFilterOperators: STOCK_FILTER_OPERATORS,
      showBackToTop: false,
      descripSearch: null,
      descripResults: [],
      descripLoading: false,
      descripFailed: false,
      descripRequestId: 0,
      descripTimer: null,
    }
  },

  computed: {
    ...mapGetters('saleapp/categories', ['getSelectedBrands', 'isListView']),

    ...mapGetters('saleapp/products', [
      'getAllProducts',
      'getSearchProduct',
      'getItemImages',
      'getIsLoadingMore',
      'getAllDataLoaded',
      'getHasNextPage',
      'getStockFilters',
      'getIsLoading',
    ]),

    isLoadingMore() {
      return this.getIsLoadingMore
    },

    allDataLoaded() {
      return this.getAllDataLoaded
    },
    isLoading() {
      return this.getIsLoading
    },
    activeStockFilterCount() {
      // Filter count for active stock filters
      const fc =
        STOCK_FILTER_METRICS.filter(
          (metric) => this.getStockFilters[metric.field].operator
        ).length +
        TEXT_FILTER_FIELDS.filter(
          (textFilter) => this.getStockFilters[textFilter.field]
        ).length +
        (this.getStockFilters.descrips.length > 0 ||
        this.getStockFilters.descripText
          ? 1
          : 0) +
        (this.getStockFilters.skuPrefix ? 1 : 0)
      this.$store.dispatch('saleapp/products/setActiveStockFilterCount', fc)
      return fc
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

    showPanelFilters() {
      return this.$store.state.saleapp.products.showPanelFilters
    },

    descripOptions() {
      // Selected texts stay in the list so their chips survive new searches.
      const selected = this.stockFilterDraft.descrips
      const selectedNames = new Set(selected)
      const known = new Map(this.descripResults.map((d) => [d.name, d]))
      return [
        ...selected.map((name) => known.get(name) || { name }),
        ...this.descripResults.filter((d) => !selectedNames.has(d.name)),
      ]
    },

    descripNoDataText() {
      const query = (this.descripSearch || '').trim()
      if (query.length < DESCRIP_SEARCH_MIN_LENGTH) {
        return `Type at least ${DESCRIP_SEARCH_MIN_LENGTH} characters`
      }
      if (this.descripLoading) return 'Searching...'
      return this.descripFailed
        ? 'Suggestions are unavailable'
        : 'No matching descriptions'
    },

    descripHint() {
      const text = (this.descripSearch || '').trim()
      if (!text) return ''
      return this.stockFilterDraft.descrips.length > 0
        ? 'Typed text is ignored while items are selected'
        : `Apply to match descriptions containing "${text}"`
    },

    descripMenuProps() {
      return {
        maxHeight: this.$vuetify.breakpoint.mobile ? 220 : 300,
        closeOnContentClick: false,
      }
    },

    descripVisibleChips() {
      return this.$vuetify.breakpoint.mobile ? 1 : 2
    },
  },

  watch: {
    filteredItems(newVal) {
      this.setCountFilteredProducts(newVal?.length)
    },
    showPanelFilters(newVal) {
      if (newVal) {
        this.openStockFilters()
      }
    },
    stockFiltersOpen(newVal) {
      if (!newVal && this.showPanelFilters) {
        this.$store.dispatch('saleapp/products/setShowPanelFilters')
      }
    },
    descripSearch(value) {
      this.onDescripSearch(value)
    },
  },

  beforeMount() {
    this.$store.dispatch('sistema/setShowBottomNav', false)
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
    clearTimeout(this.descripTimer)
    this.$store.dispatch('sistema/setShowBottomNav', true)
  },

  methods: {
    ...mapActions('saleapp/products', [
      'setCountFilteredProducts',
      'loadMoreProducts',
      'fetchProducts',
      'fetchProductSuggestions',
    ]),

    openStockFilters() {
      this.stockFilterDraft = cloneStockFilters(this.getStockFilters)
      this.stockFilterError = ''
      this.descripSearch = this.getStockFilters.descripText || null
      this.descripResults = []
      this.descripFailed = false
      this.stockFiltersOpen = true
    },

    onDescripSearch(value) {
      clearTimeout(this.descripTimer)
      const query = (value || '').trim()

      // Bumping the id invalidates any request still in flight.
      if (query.length < DESCRIP_SEARCH_MIN_LENGTH) {
        this.descripRequestId++
        this.descripResults = []
        this.descripLoading = false
        this.descripFailed = false
        return
      }

      this.descripLoading = true
      this.descripTimer = setTimeout(
        () => this.loadDescripSuggestions(query),
        DESCRIP_SEARCH_DELAY
      )
    },

    async loadDescripSuggestions(query) {
      const requestId = ++this.descripRequestId
      try {
        const results = await this.fetchProductSuggestions(query)
        if (requestId !== this.descripRequestId) return

        this.descripFailed = false
        this.descripResults = results
          .filter((d) => d && d.name)
          .map((d) => ({
            name: String(d.name),
            products: Number(d.products) || 0,
          }))
      } catch (error) {
        if (requestId === this.descripRequestId) {
          this.descripFailed = true
          this.descripResults = []
        }
      } finally {
        if (requestId === this.descripRequestId) this.descripLoading = false
      }
    },

    removeDescrip(name) {
      this.stockFilterDraft.descrips = this.stockFilterDraft.descrips.filter(
        (text) => text !== name
      )
    },

    closeStockFilters() {
      this.stockFiltersOpen = false
      // this.$store.dispatch('saleapp/products/setShowPanelFilters')
    },

    async applyStockFilters() {
      if (this.stockFilterDraft.descrips.length > MAX_DESCRIP_FILTERS) {
        this.stockFilterError = `Description: select at most ${MAX_DESCRIP_FILTERS} items.`
        return
      }

      const typedText = (this.descripSearch || '').trim()
      if (
        !this.stockFilterDraft.descrips.length &&
        typedText.length > DESCRIP_TEXT_MAX_LENGTH
      ) {
        this.stockFilterError = `Description: text must have at most ${DESCRIP_TEXT_MAX_LENGTH} characters.`
        return
      }
      const skuPrefix = String(this.stockFilterDraft.skuPrefix || '').trim()
      if (skuPrefix.length > 50) {
        this.stockFilterError = 'SKU prefix must have at most 50 characters.'
        return
      }

      const filters = {
        descrips: [...this.stockFilterDraft.descrips],
        // Typed text only filters when nothing was selected.
        descripText: this.stockFilterDraft.descrips.length ? '' : typedText,
        skuPrefix,
      }

      for (const textFilter of TEXT_FILTER_FIELDS) {
        filters[textFilter.field] = String(
          this.stockFilterDraft[textFilter.field] || ''
        ).trim()
      }

      for (const metric of STOCK_FILTER_METRICS) {
        const criterion = this.stockFilterDraft[metric.field]
        if (!criterion.operator) continue

        if (
          criterion.value === '' ||
          !Number.isSafeInteger(Number(criterion.value))
        ) {
          this.stockFilterError = `${metric.label}: ingresa una cantidad entera.`
          return
        }

        const value = Number(criterion.value)
        let valueTo
        if (criterion.operator === 'between') {
          if (
            criterion.valueTo === '' ||
            !Number.isSafeInteger(Number(criterion.valueTo))
          ) {
            this.stockFilterError = `${metric.label}: completa ambos límites con enteros.`
            return
          }
          valueTo = Number(criterion.valueTo)
          if (value > valueTo) {
            this.stockFilterError = `${metric.label}: el límite inicial debe ser menor o igual al final.`
            return
          }
        }

        filters[metric.field] = {
          operator: criterion.operator,
          value,
          valueTo,
        }
      }

      this.stockFilterError = ''
      try {
        await this.fetchProducts({ page: 1, resetData: true, filters })
        this.stockFiltersOpen = false
        // this.$store.dispatch('saleapp/products/setShowPanelFilters')
        window.scrollTo(0, 0)
        this.$nextTick(() => this.checkScrollPosition())
      } catch (error) {
        this.stockFilterError = 'No se pudieron cargar los productos filtrados.'
      }
    },

    clearStockFilters() {
      this.stockFilterDraft = emptyStockFilters()
      this.descripSearch = null
      this.stockFilterError = ''
      return this.applyStockFilters()
    },

    async loadSlideshow(src) {
      await this.$store.dispatch('saleapp/products/fetchItemImages', src)
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
      this.showBackToTop = scrollTop > BACK_TO_TOP_THRESHOLD

      // Detectar si estamos cerca del final (200px antes del final)
      const threshold = 200
      const nearBottom = scrollTop + clientHeight >= scrollHeight - threshold

      if (nearBottom && this.shouldLoadMore()) {
        this.loadMore()
      }
    },

    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' })
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

.stock-filter-toolbar {
  display: flex;
  justify-content: flex-end;
  padding: 8px 16px 0;
}

.stock-filter-sheet {
  max-height: 85vh;
  max-width: 680px;
  overflow-y: auto;
  padding: 16px;
}

.stock-filter-heading,
.stock-filter-actions {
  align-items: center;
  display: flex;
}

.stock-filter-heading {
  justify-content: space-between;
}

.stock-filter-heading h2 {
  font-size: 20px;
  font-weight: 500;
}

.stock-filter-row {
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  min-height: 64px;
}

.operator-symbol {
  display: inline-block;
  font-size: 18px;
  font-weight: 600;
  min-width: 2rem;
  text-align: center;
}

.descrip-chip-text {
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.back-to-top {
  bottom: calc(16px + env(safe-area-inset-bottom)) !important;
  right: calc(16px + env(safe-area-inset-right)) !important;
}

@media (max-width: 600px) {
  .stock-filter-toolbar {
    padding: 4px 8px 0;
  }

  .stock-filter-sheet {
    max-height: 90vh;
    padding: 12px;
  }
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
