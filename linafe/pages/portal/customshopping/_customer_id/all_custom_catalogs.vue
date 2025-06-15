<template>
  <div>
    <h1>All Custom Catalogs</h1>
    <p>
      Aquí puedes ver todos los catálogos personalizados para
      {{ $route.params.customer_id }}.
    </p>
    <v-row>
      <v-col cols="12">
        <div v-if="isListView">
          <v-list three-line class="mx-0">
            <CategoryListItem
              v-for="item in filteredItems"
              :key="item.id"
              :category="{ ...item, type: 'depto', link: setLink(item.token) }"
              @card-clicked="setSelectProductsByElement"
            />
          </v-list>
        </div>
        <div v-else class="shopping-cart mt-4">
          <CategoryCard
            v-for="item in filteredItems"
            :key="item.id"
            :category="{ ...item, type: 'depto', link: setLink(item.token) }"
            @card-clicked="setSelectProductsByElement"
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

  async asyncData({ store, error }) {
    try {
      // await store.dispatch('shoppingcart/categories/fetchItems', {
      //   name: 'Department',
      // })
      await store.dispatch('shoppingcart/categories/fetchData', {
        name: 'Catalog',
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
    return {
      link: '/shoppingcart/categories/categoriesmain',
    }
  },

  computed: {
    ...mapGetters('shoppingcart/categories', [
      'getSelectedBrands',
      'getSearchDepartment',
      'getAllDepartments',
      'getViewConfElement',
      'isListView',
    ]),

    ...mapGetters({ customerId: 'customshopping/customcatalog/getCustomerId' }),

    filteredItems() {
      return this.getAllDepartments.filter((item) => {
        const selectedBrands = this.getSelectedBrands
        let searchDepartment = this.getSearchDepartment

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
  },

  watch: {
    filteredItems(newVal) {
      this.setCountFilteredDep(newVal?.length)
    },
  },

  mounted() {
    window.scrollTo(0, 0)
    this.setCountFilteredDep(this.filteredItems?.length)
  },

  methods: {
    ...mapActions('shoppingcart/categories', [
      'setSelectProductsByElement',
      'setCountFilteredDep',
    ]),
    setLink(catalogToken) {
      return (
        `/portal/customshopping/${this.customerId}/${catalogToken}` ?? this.link
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
