<template>
  <div>
    <div class="floating-header">
      <v-row>
        <v-toolbar flat color="rgba(225, 250, 250, 0.5)">
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                class="mt-0 mb-2 mx-2"
                icon
                v-bind="attrs"
                color="cyan lighten-1"
                v-on="on"
                @click="$router.back()"
              >
                <v-icon>mdi-chevron-left</v-icon>
              </v-btn>
            </template>
            <span>Volver a vista anterior</span>
          </v-tooltip>
          <v-select
            v-model="selected_brands"
            :items="brands"
            multiple
            label="Filter by brand"
            chips
            deletable-chips
            dense
          ></v-select>
          <v-spacer></v-spacer>
          <v-text-field
            v-show="cur_child_view.includes('departments')"
            id="depatments"
            v-model="search_department"
            solo
            flat
            hide-details
            prepend-inner-icon="mdi-magnify"
            label="Search"
            dense
            rounded
            clearable
          ></v-text-field>
          <v-text-field
            v-show="cur_child_view.includes('categoriesmain')"
            id="categories"
            v-model="search_category"
            solo
            flat
            hide-details
            prepend-inner-icon="mdi-magnify"
            label="Search"
            dense
            rounded
            clearable
          ></v-text-field>
          <v-text-field
            v-show="cur_child_view.includes('categoriessub')"
            id="subcategories"
            v-model="search_subcategory"
            solo
            flat
            hide-details
            prepend-inner-icon="mdi-magnify"
            label="Search"
            dense
            rounded
            clearable
          ></v-text-field>
          <v-text-field
            v-show="cur_child_view.includes('products')"
            id="products"
            v-model="search_product"
            solo
            flat
            hide-details
            prepend-inner-icon="mdi-magnify"
            label="Search"
            dense
            rounded
            clearable
          ></v-text-field>
          <v-btn class="ma-2" icon color="cyan lighten-1">
            <v-icon>mdi-format-list-text</v-icon>
          </v-btn>
          <v-menu offset-y>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                class="mr-2"
                icon
                color="cyan lighten-1"
                v-bind="attrs"
                v-on="on"
              >
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item @click="goToCart">
                <v-list-item-title>Go to Cart</v-list-item-title>
              </v-list-item>
              <v-list-item @click="snackbar = true">
                <v-list-item-title>Option 2</v-list-item-title>
              </v-list-item>
              <v-list-item @click="snackbar = true">
                <v-list-item-title>Option 3</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-toolbar>
      </v-row>
      <v-row>
        <div v-if="crumbs.length > 0">
          <v-breadcrumbs :items="crumbs" nuxt></v-breadcrumbs>
        </div>
      </v-row>
    </div>
    <div>
      <nuxt-child></nuxt-child>
    </div>
    <v-snackbar v-model="snackbar" timeout="2000">
      No implementado
      <template v-slot:action="{ attrs }">
        <v-btn
          color="secondary"
          text
          v-bind="attrs"
          @click.stop="snackbar = false"
        >
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  data() {
    return {
      brands: ['Brand 1', 'Brand 2', 'Brand 3', 'Brand 4', 'Brand 5'],
      selected_brands: [],
      cur_child_view: 'departments',
      search_department: '',
      search_category: '',
      search_subcategory: '',
      search_product: '',
      breadcrumbs: [],
      snackbar: false,
    }
  },

  computed: {
    ...mapGetters('shoppingcart/categories', [
      'getSelectedBrands',
      'getSearchDepartment',
      'getSearchCategory',
      'getSearchSubcategory',
      'getSearchProduct',
    ]),
    crumbs() {
      const n = this.$route.fullPath.lastIndexOf('/')
      const curText = () => {
        switch (this.$route.fullPath.substring(n + 1)) {
          case 'departments':
            return 'Departments'
          case 'categoriesmain':
            return 'Categories'
          case 'categoriessub':
            return 'Subcategories'
          case 'products':
            return 'Products'
          default:
            return ''
        }
      }

      const crumbs = this.breadcrumbs

      if (crumbs.length > 0) {
        crumbs.forEach((e) => {
          e.disabled = false
        })
      }

      const index = crumbs.findIndex((crumb) => crumb.text === curText())
      const crumb = index !== -1 ? crumbs[index] : null

      if (crumb) {
        crumb.disabled = true
        if (crumbs.length > index + 1) {
          crumbs.splice(index + 1, crumbs.length - index - 1)
        }
      } else {
        crumbs.push({
          text: curText(),
          disabled: true,
          to: this.$route.fullPath,
        })
      }

      return crumbs
    },
  },

  watch: {
    $route(to) {
      this.cur_child_view = to.name
    },
    selected_brands(newVal) {
      this.setSelectedBrands(newVal)
    },
    search_department(newVal) {
      this.setSearchDepartment(newVal)
    },
    search_category(newVal) {
      this.setSearchCategory(newVal)
    },
    search_subcategory(newVal) {
      this.setSearchSubcategory(newVal)
    },
    search_product(newVal) {
      this.setSearchProduct(newVal)
    },
  },

  mounted() {
    this.setShowBottomNav(true)
  },

  methods: {
    ...mapActions('shoppingcart/categories', [
      'setSelectedBrands',
      'setSearchDepartment',
      'setSearchCategory',
      'setSearchSubcategory',
      'setSearchProduct',
    ]),
    ...mapActions('sistema', ['setShowBottomNav']),
    goToCart() {
      this.$router.push('/shoppingcart/cart')
    },
  },
}
</script>

<style scoped>
.floating-header {
  position: -webkit-sticky; /* Safari */
  position: sticky;
  top: 45px; /* Ajusta este valor según la altura de tu app-bar */
  z-index: 3; /* Asegúrate de que esté por encima de otros elementos */
  background-color: white;
}
</style>
