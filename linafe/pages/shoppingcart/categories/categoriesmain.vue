<template>
  <div>
    <v-row>
      <v-col cols="12">
        <div v-if="isListView">
          <v-list three-line class="mx-0">
            <CategoryListItem
              v-for="item in filteredItems"
              :key="item.id"
              :category="{ ...item, type: 'cat', link: setLink() }"
              @card-clicked="setSelectProductsByElement"
            />
          </v-list>
        </div>
        <div v-else class="shopping-cart mt-4">
          <CategoryCard
            v-for="item in filteredItems"
            :key="item.id"
            :category="{ ...item, type: 'cat', link: setLink() }"
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
  name: 'CategoriesMain',
  components: {
    CategoryCard,
    CategoryListItem,
  },
  async asyncData({ store, error }) {
    try {
      await store.dispatch('shoppingcart/categories/fetchItems', {
        name: 'Category',
      })
      // await store.dispatch('shoppingcart/categories/fetchData', {
      //   name: 'Category',
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
      link: '/shoppingcart/categories/categoriessub',
    }
  },

  computed: {
    ...mapGetters('shoppingcart/categories', [
      'getSelectedBrands',
      'getSearchCategory',
      'getAllCategories',
      'getViewConfElement',
      'isListView',
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
            item.brands
              .split(',')
              .some((brand) => selectedBrands.includes(brand))
          )
        }

        return item.name.toLowerCase().includes(searchCategory.toLowerCase())
      })
    },
  },

  watch: {
    filteredItems(newVal) {
      this.setCountFilteredCat(newVal?.length)
    },
  },

  mounted() {
    window.scrollTo(0, 0)
    this.setCountFilteredCat(this.filteredItems?.length)
  },

  methods: {
    ...mapActions('shoppingcart/categories', [
      'setSelectProductsByElement',
      'setCountFilteredCat',
    ]),
    setLink() {
      return this.getViewConfElement('link', 'configval2') ?? this.link
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
