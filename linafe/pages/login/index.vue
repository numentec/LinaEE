<template>
  <v-row justify="center" align="center">
    <v-col cols="12">
      <UserLogin class="mt-5" />
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'LoginPage',
  layout: 'login',
  components: {
    UserLogin: () => import('~/components/core/UserLogin.vue'),
  },
  computed: {
    is_screen_small() {
      return this.$vuetify.breakpoint.smAndDown
    },
  },
  mounted() {
    // const curuser = localStorage.getItem('curuser')
    // if (curuser) {
    //   this.$store.dispatch('sistema/setUserData', curuser).then(() => {
    //     if (this.$nuxt.$route.name === 'login') {
    //       this.$router.push('/')
    //     }
    //   })
    //   // this.$auth.setUser(curuser)
    //   // this.$store.commit('sistema/SET_USER_DATA', curuser)
    // }
  },
  head() {
    return {
      title: 'Login',
    }
  },
}
</script>

<style></style>
