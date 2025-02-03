<template>
  <div class="shopping-cart mt-4">
    <div v-for="(item, index) in filteredItems" :key="index">
      <CategoryCard
        :category="{ ...item, type: 'depto', link: setLink() }"
        @card-clicked="setSelectProductsByElement"
      />
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import CategoryCard from '~/components/shoppingcart/CategoryCard.vue'

export default {
  components: {
    CategoryCard,
  },

  async asyncData({ store, error }) {
    try {
      await store.dispatch('shoppingcart/categories/fetchItems', {
        name: 'Department',
      })
      // await store.dispatch('shoppingcart/categories/fetchData', {
      //   name: 'Department',
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
    ]),

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

  mounted() {
    window.scrollTo(0, 0)
    // console.log(
    //   'Departments mounted with:',
    //   this.getViewConfElement('link', 'configval1')
    // )
  },

  methods: {
    ...mapActions('shoppingcart/categories', ['setSelectProductsByElement']),
    setLink() {
      return this.getViewConfElement('link', 'configval1') ?? this.link
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
