<template>
  <div class="shopping-cart mt-4">
    <div v-for="(item, index) in filteredItems" :key="index">
      <CategoryCard :category="{ ...item, link }" />
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
      await store.dispatch('shoppingcart/categories/fetchItems', {
        name: 'Category',
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
      link: '/shoppingcart/categories/categoriessub',
    }
  },

  computed: {
    ...mapGetters('shoppingcart/categories', [
      'getSelectedBrands',
      'getSearchCategory',
      'getAllCategories',
    ]),
    filteredItems() {
      return this.getAllCategories.filter((item) => {
        const selectedBrands = this.getSelectedBrands
        let searchCategory = this.getSearchCategory

        if (searchCategory === null || searchCategory === undefined) {
          searchCategory = ''
        }

        if (searchCategory === '' && selectedBrands.length === 0) {
          return true
        }

        if (selectedBrands.length > 0) {
          return (
            item.name.toLowerCase().includes(searchCategory.toLowerCase()) &&
            selectedBrands.includes(item.brands[0])
          )
        }

        return item.name.toLowerCase().includes(searchCategory.toLowerCase())
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
