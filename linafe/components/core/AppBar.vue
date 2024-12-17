/* eslint-disable no-console */
<template>
  <div>
    <v-app-bar id="app-bar" color="primary" clipped-left fixed app dense dark>
      <v-btn icon @click="setMiniState(!is_mini)">
        <v-icon>
          {{ `${is_expanded ? 'mdi-backburger' : 'mdi-menu'}` }}
        </v-icon>
      </v-btn>
      <v-menu bottom right>
        <template v-slot:activator="{ on: menu, attrs }">
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn
                text
                dark
                x-large
                v-bind="attrs"
                v-on="{ ...tooltip, ...menu }"
              >
                {{ getCurCia ? getCurCia.nombre_corto : 'LinaEE' }}
              </v-btn>
            </template>
            <span>Compañía actual</span>
          </v-tooltip>
        </template>
        <v-list>
          <AppBarItem v-for="(cia, i) in getCias" :key="i">
            <v-list-item-title @click="setCurCia(cia)">
              {{ cia.nombre_corto }}
            </v-list-item-title>
          </AppBarItem>
        </v-list>
      </v-menu>
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
      <v-menu offset-y origin="center center" transition="scale-transition">
        <template v-slot:activator="{ on: menu, attrs }">
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-avatar
                color="accent"
                size="35"
                v-bind="attrs"
                v-on="{ ...tooltip, ...menu }"
              >
                <img v-if="loggedInUser.foto" :src="imgSrc" alt="U" />
                <v-icon v-else dark>mdi-account-circle</v-icon>
              </v-avatar>
            </template>
            <span>{{ capUserName }}</span>
          </v-tooltip>
        </template>
        <v-list>
          <AppBarItem>
            <v-list-item-title @click="goProfile">Perfil</v-list-item-title>
          </AppBarItem>
          <AppBarItem>
            <v-list-item-title @click.stop="userLogout">
              Cerrar Sesión
            </v-list-item-title>
          </AppBarItem>
        </v-list>
      </v-menu>
    </v-app-bar>
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex'
// Components
import { VHover, VListItem } from 'vuetify/lib'
// import { authComputed } from '~/store/core.js'

export default {
  name: 'CoreAppBar',

  components: {
    AppBarItem: {
      render(h) {
        return h(VHover, {
          scopedSlots: {
            default: ({ hover }) => {
              return h(
                VListItem,
                {
                  attrs: this.$attrs,
                  class: {
                    'black--text': !hover,
                    'white--text secondary elevation-12': hover,
                  },
                  props: {
                    activeClass: '',
                    dark: hover,
                    link: true,
                    ...this.$attrs,
                  },
                },
                this.$slots.default
              )
            },
          },
        })
      },
    },
  },

  data() {
    return {
      title: 'LinaEE',
    }
  },

  computed: {
    ...mapState('core', ['drawer', 'is_mini', 'is_expanded']),
    ...mapState('sistema', ['curuser']),
    ...mapGetters(['isAuthenticated', 'loggedInUser']),
    ...mapGetters('sistema', ['getUsers', 'getCias', 'getCurCia']),
    ...mapGetters('shoppingcart/cart', [
      'getCartItemCount',
      'getCartProductCount',
    ]),
    imgSrc() {
      return this.$config.publicURL + this.loggedInUser.foto
    },
    capUserName() {
      const lu = this.loggedInUser.username
      if (lu) {
        return lu.charAt(0).toUpperCase() + lu.slice(1)
      }
      return 'U'
    },
  },

  methods: {
    ...mapActions('core', ['setDrawer', 'setIsMini', 'setIsExpanded']),
    ...mapActions('sistema', ['userLogout', 'userProfile', 'setCurCia']),
    goProfile() {
      const curID = this.loggedInUser.id
      if (this.getUsers.length === 0) {
        this.userProfile(curID).then(() => {
          this.$router.push({
            path: '/sistema/usuarios/' + curID,
          })
        })
      } else {
        this.$router.push({ path: '/sistema/usuarios/' + curID })
      }
    },
    setMiniState(mini) {
      this.setIsMini(mini)
      this.setIsExpanded(!mini)
      this.setDrawer(!this.drawer)
    },
    goToCart() {
      this.$router.push('/shoppingcart/cart')
    },
  },
}
</script>
