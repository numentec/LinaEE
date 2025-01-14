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

        const lastRoute = localStorage.getItem('lina_lastRoute')
        if (lastRoute && lastRoute !== this.$route.fullPath) {
          this.$router.push(lastRoute)
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
