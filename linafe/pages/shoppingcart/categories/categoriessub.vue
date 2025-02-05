<template>
  <div class="shopping-cart mt-4">
    <div v-for="(item, index) in filteredItems" :key="index">
      <CategoryCard
        :category="{ ...item, type: 'scat', link: setLink() }"
        @card-clicked="setSelectProductsByElement"
      />
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import CategoryCard from '~/components/shoppingcart/CategoryCard.vue'

export default {
  name: 'CategoriesSub',
  components: {
    CategoryCard,
  },
  async asyncData({ store, error }) {
    try {
      await store.dispatch('shoppingcart/categories/fetchItems', {
        name: 'Subcategory',
      })
      // await store.dispatch('shoppingcart/categories/fetchData', {
      //   name: 'Subcategory',
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
      link: '/shoppingcart/categories/products',
    }
  },

  computed: {
    ...mapGetters('shoppingcart/categories', [
      'getSelectedBrands',
      'getSearchSubcategory',
      'getAllSubcategories',
      'getViewConfElement',
    ]),

    filteredItems() {
      return this.getAllSubcategories.filter((item) => {
        const selectedBrands = this.getSelectedBrands
        let searchSubCategory = this.getSearchSubcategory

        if (searchSubCategory === null || searchSubCategory === undefined) {
          searchSubCategory = ''
        }

        if (searchSubCategory === '' && selectedBrands.length === 0) {
          return true
        }

        if (selectedBrands.length > 0) {
          return (
            item.name.toLowerCase().includes(searchSubCategory.toLowerCase()) &&
            item.brands
              .split(',')
              .some((brand) => selectedBrands.includes(brand))
          )
        }

        return item.name.toLowerCase().includes(searchSubCategory.toLowerCase())
      })
    },
  },

  watch: {
    filteredItems(newVal) {
      this.setCountFilteredSubcat(newVal?.length)
    },
  },

  mounted() {
    window.scrollTo(0, 0)
    this.setCountFilteredSubcat(this.filteredItems?.length)
  },
  methods: {
    ...mapActions('shoppingcart/categories', [
      'setSelectProductsByElement',
      'setCountFilteredSubcat',
    ]),
    onImgError() {
      this.imgSrc = '/no_image.png'
    },
    setLink() {
      return this.getViewConfElement('link', 'configval3') ?? this.link
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
