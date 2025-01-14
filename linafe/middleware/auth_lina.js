export default function ({ $auth, store, redirect, route }) {
  if (!process.server) {
    const curuser = localStorage.getItem('curuser')
    if (curuser) {
      const cu = JSON.parse(curuser)
      this.$store.dispatch('sistema/setUserData', cu).then(() => {
        if (cu.homelink) {
          this.$router.push(cu.homelink)
        } else {
          this.$router.push('/')
        }
      })
    }
  }
}
