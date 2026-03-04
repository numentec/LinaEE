<template>
  <v-row justify="center" align="center">
    <v-col cols="12">
      <UserLogin v-show="!isAuthenticated" class="mt-5" />
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'LoginPage',
  layout: 'login',
  components: {
    UserLogin: () => import('~/components/core/UserLogin.vue'),
  },
  data() {
    return {
      previousPath: null,
    }
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      vm.previousPath = from && from.fullPath ? from.fullPath : null
    })
  },
  computed: {
    ...mapGetters(['loggedInUser', 'isAuthenticated']),
    is_screen_small() {
      return this.$vuetify.breakpoint.smAndDown
    },
  },
  mounted() {
    const curuser = localStorage.getItem('lina_curuser')

    if (curuser) {
      const cu = JSON.parse(curuser)
      this.$store.dispatch('sistema/setUserData', cu).then(() => {
        this.nuxtClientInit()

        const queryRedirect = this.$route.query.redirect
        const redirectPath =
          typeof queryRedirect === 'string' && queryRedirect.startsWith('/')
            ? queryRedirect
            : null
        const lastPath = localStorage.getItem('lina_lastPath')
        const fullPath = this.$route.fullPath

        if (
          redirectPath &&
          redirectPath !== fullPath &&
          !redirectPath.startsWith('/login')
        ) {
          this.$router.push(redirectPath)
        } else if (lastPath && lastPath !== fullPath) {
          this.$router.push(lastPath)
        } else if (cu.homelink) {
          this.$router.push(cu.homelink)
        } else {
          this.$router.push('/')
        }
      })
    }
  },
  methods: {
    ...mapActions(['nuxtClientInit']),
  },
  head() {
    return {
      title: 'Login',
    }
  },
}
</script>

<style></style>
