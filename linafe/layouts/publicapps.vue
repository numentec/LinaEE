<template>
  <v-app id="publicapps">
    <v-app-bar color="primary" clipped-left fixed app dark>
      <v-app-bar-nav-icon icon @click="setMiniState(!is_mini)">
        <v-icon>
          {{ `${is_expanded ? 'mdi-backburger' : 'mdi-menu'}` }}
        </v-icon>
      </v-app-bar-nav-icon>
      <v-toolbar-title>LinaEE Customer Portal</v-toolbar-title>
      <v-spacer />
      <v-badge
        v-show="getCartItemCount > 0"
        :content="getCartProductCount > 999 ? '999+' : getCartProductCount"
        class="mr-6"
        color="red"
        offset-y="25"
        overlap
      >
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon dark v-bind="attrs" v-on="on" @click="goToCart">
              <v-icon dark>mdi-cart-outline</v-icon>
            </v-btn>
          </template>
          <span>Go to cart</span>
        </v-tooltip>
      </v-badge>
      <v-card-actions>
        <v-btn rounded small color="success" @click="$router.push('/login')">
          <v-icon left> mdi-account-key </v-icon>
          Login
        </v-btn>
      </v-card-actions>
      <v-btn icon @click="$router.push('/login')">
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>
    </v-app-bar>
    <component
      :is="useDrawer.component"
      ref="appdrawerx"
      v-bind="useDrawer.props"
    />
    <v-main class="grey lighten-3">
      <v-container>
        <nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex'
import DrawerCatalog from '../components/customcatalog/DrawerCatalog.vue'

const CoreDrawer = () => import('../components/core/Drawer')
const CoreDrawerMobile = () => import('../components/core/DrawerMobile')

export default {
  name: 'PortalLayout',
  components: {
    DrawerCatalog,
  },
  data: () => ({}),

  computed: {
    ...mapState('core', ['drawer', 'is_mini', 'is_expanded']),
    ...mapGetters('shoppingcart/cart', [
      'getCartItemCount',
      'getCartProductCount',
    ]),
    ...mapGetters({ customerId: 'customshopping/customcatalog/getCustomerId' }),
    useDrawer() {
      if (this.$vuetify.breakpoint.mobile) {
        return {
          component: CoreDrawerMobile,
          props: {
            drawerListComponent: DrawerCatalog,
          },
        }
      } else {
        return {
          component: CoreDrawer,
          props: {
            drawerListComponent: DrawerCatalog,
          },
        }
      }
    },
  },

  methods: {
    ...mapActions('core', ['setDrawer', 'setIsMini', 'setIsExpanded']),
    setMiniState(mini) {
      this.setIsMini(mini)
      this.setIsExpanded(!mini)
      this.setDrawer(!this.drawer)
    },
    toggleDrawer() {
      this.setDrawer(!this.drawer)
    },
    goToCart() {
      this.$router.push(`/portal/customshopping/${this.customerId}/cart`)
    },
  },
}
</script>

<style lang="scss" scoped></style>
