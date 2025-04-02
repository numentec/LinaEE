<template>
  <div>
    <div class="floating-header">
      <v-row>
        <v-toolbar flat color="rgba(225, 250, 250, 0.5)">
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                class="mt-0 mb-2"
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
          <v-autocomplete
            v-show="!isMobile"
            v-model="selected_brands"
            label="Brands"
            :items="getBrands"
            item-text="name"
            item-value="id"
            multiple
            chips
            deletable-chips
            dense
            rounded
            clearable
            background-color="white"
            single-line
            max-width="300"
            class="px-2 mt-4"
          ></v-autocomplete>
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
          <v-btn
            v-show="!isMobile"
            class="ma-2"
            icon
            color="cyan lighten-1"
            @click="toggleView"
          >
            <v-icon>{{ viewModeIcon }}</v-icon>
          </v-btn>
          <v-menu offset-y>
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon color="cyan lighten-1" v-bind="attrs" v-on="on">
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item @click="goToCart">
                <v-list-item-title>Go to Cart</v-list-item-title>
              </v-list-item>
              <v-list-item @click="toggleView">
                <v-list-item-title>
                  {{ isListView ? 'Grid view' : 'List view' }}
                </v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-list-item-action>
                  <div class="px-2">
                    <v-autocomplete
                      v-model="selected_brands"
                      label="Brands"
                      :items="getBrands"
                      item-text="name"
                      item-value="id"
                      multiple
                      chips
                      deletable-chips
                      dense
                      rounded
                      clearable
                      background-color="white"
                      single-line
                      max-width="300"
                    ></v-autocomplete>
                  </div>
                </v-list-item-action>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-toolbar>
      </v-row>
      <v-row justify="space-between">
        <div v-if="crumbs.length > 0">
          <v-breadcrumbs :items="crumbs" nuxt></v-breadcrumbs>
        </div>
        <div>
          <p
            v-show="countChildItems > 0"
            :class="[isXSScreen ? 'primary-text-xs' : 'primary-text my-2']"
          >
            {{ `${countChildItems} ${countChildItems > 1 ? 'Items' : 'Item'}` }}
          </p>
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

function uniqByKeepLast(data, key) {
  return [...new Map(data.map((x) => [key(x), x])).values()]
}

export default {
  name: 'Categories',
  components: {},
  async asyncData({ $axios, store, error }) {
    const loggedInUser = store.getters.loggedInUser
    const groupList = loggedInUser.ugroups.toString()

    try {
      const [resp0, resp1] = await Promise.all([
        $axios.get('vistas/35/'),
        $axios.get('accviewconf-list/', {
          params: { idvista: '35', groups: groupList },
        }),
        store.dispatch('shoppingcart/categories/fetchItems', { name: 'Brand' }),
      ])
      const filterPerms = uniqByKeepLast(resp1.data, (it) => it.vistaconf)
      const viewConf = resp0.data.configs_x_vista

      store.dispatch('shoppingcart/categories/setViewConf', viewConf)

      return {
        curView: {
          num: resp0.data.id,
          checkelperms: resp0.data.checkelperms,
        },
        viewConf,
        filterPerms,
      }
    } catch (err) {
      if (err.response) {
        error({
          statusCode: err.response.status,
          message: err.response.data.message,
        })
      } else if (error.request) {
        error({
          statusCode: 503,
          message: 'No hubo respuesta del servidor',
        })
      } else {
        error({
          statusCode: 1010,
          message: err.message,
        })
      }
    }
  },
  data() {
    return {
      selected_brands: [],
      cur_child_view: '',
      search_department: '',
      search_category: '',
      search_subcategory: '',
      search_product: '',
      snackbar: false,
    }
  },

  computed: {
    ...mapGetters('shoppingcart/categories', [
      'getSelectedBrands',
      'getSearchDepartment',
      'getSearchCategory',
      'getSearchSubcategory',
      'getBrands',
      'getBreadcrumbs',
      'getCountFilteredDep',
      'getCountFilteredCat',
      'getCountFilteredSubcat',
      'getSelectedCategoryName',
      'isListView',
    ]),
    ...mapGetters('shoppingcart/products', [
      'getSearchProduct',
      'getCountFilteredProducts',
    ]),
    isMobile() {
      return this.$vuetify.breakpoint.mobile
    },
    isXSScreen() {
      return this.$vuetify.breakpoint.xs
    },
    viewModeIcon() {
      return this.isListView ? 'mdi-view-grid' : 'mdi-format-list-text'
    },
    crumbs() {
      let curText = this.$route.query.category

      if (!curText) {
        return []
      }

      if (this.isMobile) {
        curText = curText.substring(0, 5)
      }

      curText = curText.charAt(0).toUpperCase() + curText.slice(1)

      if (curText === 'Depar') {
        curText = 'Dep'
      }

      const crumbs = JSON.parse(JSON.stringify(this.getBreadcrumbs))

      if (crumbs.length > 0) {
        crumbs.forEach((e) => {
          e.disabled = false
        })
      }

      const index = crumbs.findIndex(
        (crumb) => crumb.to === this.$route.fullPath
      )
      const crumb = index !== -1 ? crumbs[index] : null

      if (crumb) {
        crumb.disabled = true
        if (crumbs.length > index + 1) {
          crumbs.splice(index + 1, crumbs.length - index - 1)
        }
      } else {
        crumbs.push({
          text: curText,
          disabled: true,
          to: this.$route.fullPath,
        })
      }

      this.setBreadcrumbs(JSON.parse(JSON.stringify(crumbs)))

      return crumbs
    },

    countChildItems() {
      const index = this.cur_child_view.lastIndexOf('-')
      const curChild =
        index !== -1
          ? this.cur_child_view.substring(index + 1)
          : this.cur_child_view

      switch (curChild) {
        case 'departments':
          return this.getCountFilteredDep
        case 'categoriesmain':
          return this.getCountFilteredCat
        case 'categoriessub':
          return this.getCountFilteredSubcat
        case 'products':
          return this.getCountFilteredProducts
        default:
          return 0
      }
    },
  },

  watch: {
    $route: {
      immediate: true,
      handler(to) {
        this.cur_child_view = to.name
      },
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
    // breadcrumbs(newVal) {
    //   this.$store.commit('shoppingcart/categories/SET_BREADCRUMBS', [...newVal])
    // },
  },

  mounted() {
    this.setShowBottomNav(true)
    this.setListView(this.isMobile)
  },

  methods: {
    ...mapActions('shoppingcart/categories', [
      'setSelectedBrands',
      'setSearchDepartment',
      'setSearchCategory',
      'setSearchSubcategory',
      'setBreadcrumbs',
      'setListView',
    ]),
    ...mapActions('shoppingcart/products', ['setSearchProduct']),
    ...mapActions('sistema', ['setShowBottomNav']),
    goToCart() {
      this.$router.push('/shoppingcart/cart')
    },
    toggleView() {
      this.setListView(!this.isListView)
    },
  },
}
</script>

<style scoped>
.floating-header {
  position: -webkit-sticky; /* Safari */
  position: sticky;
  top: 45px; /* Ajusta este valor según la altura de tu app-bar */
  z-index: 3; /* Asegúrate de que esté por encima de otros elementos pero por debajo del Drawer */
  background-color: white;
}
.primary-text {
  font-size: 16px;
  color: var(--v-primary-base);
}
.primary-text-xs {
  font-size: 12px;
  color: var(--v-primary-base);
}
</style>
