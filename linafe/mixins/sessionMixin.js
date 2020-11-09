export const sessionMixin = {
  mounted() {
    const curuser = localStorage.getItem('user')

    if (curuser) {
      if (this.$nuxt.$route.name.includes('/login')) {
        window.onNuxtReady(() => {
          window.$nuxt.$router.push('/')
        })
      }
    }

    if (!curuser) {
      window.onNuxtReady(() => {
        window.$nuxt.$router.push('/login')
      })
    }
  },
}
