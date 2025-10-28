<template>
  <div>
    <h1>{{ title }}</h1>
    <p>
      Aquí puedes ver todos los catálogos personalizados para
      {{ getCustomer.name }}.
    </p>
    <v-row>
      <v-col cols="12">
        <div v-if="isListView">
          <v-list three-line class="mx-0">
            <CategoryListItem
              v-for="item in filteredItems"
              :key="item.id"
              :category="{
                ...item,
                type: 'catalog',
                link: setLink(item.token),
              }"
            />
          </v-list>
        </div>
        <div v-else class="shopping-cart mt-4">
          <CategoryCard
            v-for="item in filteredItems"
            :key="item.id"
            :category="{ ...item, type: 'catalog', link: setLink(item.token) }"
          />
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import CategoryCard from '~/components/shoppingcart/CategoryCard.vue'
import CategoryListItem from '~/components/shoppingcart/CategoryListItem.vue'

export default {
  name: 'AllCustomCatalogs',
  layout: 'publicapps',
  components: {
    CategoryCard,
    CategoryListItem,
  },

  async asyncData({ params, store, error }) {
    try {
      const cULID = params.customer_ulid

      if (!cULID) {
        error({
          statusCode: 404,
          message: 'Customer ID is required',
        })
        return
      }

      await store.dispatch('customshopping/customcatalog/fetchItems', {
        ulid: cULID,
      })
      // await store.dispatch('customshopping/customcatalog/fetchData', {
      //   name: 'Catalog',
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
          message:
            'No se pudo cargar la lista. Intente luego por favor. (INDEX)',
        })
      }
    }
  },

  data() {
    return {
      link: '/login',
    }
  },

  computed: {
    ...mapGetters('customshopping/customcatalog', [
      'getSelectedBrands',
      'getSearchCustomCatalog',
      'getAllCustomCatalogs',
      'getTotalCatalogs',
      'getCustomer',
      'getCustomerULID',
      'isListView',
    ]),

    filteredItems() {
      return this.getAllCustomCatalogs.filter((item) => {
        const selectedBrands = this.getSelectedBrands
        let searchDepartment = this.getSearchCustomCatalog

        if (searchDepartment === null || searchDepartment === undefined) {
          searchDepartment = ''
        }

        if (searchDepartment === '' && selectedBrands.length === 0) {
          return true
        }

        if (selectedBrands.length > 0) {
          return (
            item.name.toLowerCase().includes(searchDepartment.toLowerCase()) &&
            item.brands
              .split(',')
              .some((brand) => selectedBrands.includes(brand))
          )
        }
        return item.name.toLowerCase().includes(searchDepartment.toLowerCase())
      })
    },

    title() {
      if (!this.getTotalCatalogs) {
        return 'No Custom Catalogs Available'
      }

      if (this.getTotalCatalogs === 1) {
        return `${this.getTotalCatalogs} Custom Catalog`
      }

      return `${this.getTotalCatalogs} Custom Catalogs`
    },
  },

  watch: {
    filteredItems(newVal) {
      this.setCountFilteredCC(newVal?.length)
    },
  },

  mounted() {
    window.scrollTo(0, 0)
    this.setCountFilteredCC(this.filteredItems?.length)
  },

  methods: {
    ...mapActions('customshopping/customcatalog', ['setCountFilteredCC']),
    setLink(catalogToken) {
      return (
        `/portal/customshopping/${this.getCustomer.ulid}/${catalogToken}` ??
        this.link
      )
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
</style>
