<template>
  <div class="shopping-cart mt-4">
    <div v-for="(item, index) in filteredItems" :key="index">
      <CategoryCard :category="item" />
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import CategoryCard from '~/components/shoppingcart/CategoryCard.vue'

export default {
  components: {
    CategoryCard,
  },
  async asyncData({ store, error }) {
    try {
      const items = await store.dispatch('shoppingcart/categories/fetchItems', {
        name: 'Department',
        link: '/shoppingcart/categories/categoriesmain',
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
      'getSearchDepartment',
    ]),

    filteredItems() {
      return this.items.filter((item) => {
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
            selectedBrands.includes(item.brands[0])
          )
        }
        return item.name.toLowerCase().includes(searchDepartment.toLowerCase())
      })
    },
  },

  mounted() {
    window.scrollTo(0, 0)
  },

  // methods: {
  //   ...mapActions('shoppingcart/categories', ['fetchCategories']),
  // },
}
</script>

<style scoped>
.shopping-cart {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
</style>
