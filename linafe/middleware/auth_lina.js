export default function ({ $auth, store, redirect, route }) {
  if (!process.server) {
    const curuser = localStorage.getItem('curuser')

    if (curuser) {
      $auth.setUser(curuser)
      if (route.path.includes('/login')) {
        return redirect('/')
      }
    }
  }

  // Do not run on server
  // if (process.server) {
  //   return
  // }

  // const curuser = localStorage.getItem('user')

  // if (curuser) {
  //   if (route.path === '/login') {
  //     return redirect('/')
  //   }
  //   return
  // }

  // if (!curuser) {
  //   return redirect('/login')
  // }
}
