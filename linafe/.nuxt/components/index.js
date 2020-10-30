export { default as Logo } from '../../components/Logo.vue'
export { default as VuetifyLogo } from '../../components/VuetifyLogo.vue'
export { default as AppBar } from '../../components/core/AppBar.vue'
export { default as Drawer } from '../../components/core/Drawer.vue'
export { default as LinaLogo } from '../../components/core/LinaLogo.vue'
export { default as MaterialCard } from '../../components/core/MaterialCard.vue'
export { default as UserLogin } from '../../components/core/UserLogin.vue'
export { default as UserRegister } from '../../components/core/UserRegister.vue'
export { default as SelCols } from '../../components/utilities/SelCols.vue'

export const LazyLogo = import('../../components/Logo.vue' /* webpackChunkName: "components/Logo" */).then(c => c.default || c)
export const LazyVuetifyLogo = import('../../components/VuetifyLogo.vue' /* webpackChunkName: "components/VuetifyLogo" */).then(c => c.default || c)
export const LazyAppBar = import('../../components/core/AppBar.vue' /* webpackChunkName: "components/core/AppBar" */).then(c => c.default || c)
export const LazyDrawer = import('../../components/core/Drawer.vue' /* webpackChunkName: "components/core/Drawer" */).then(c => c.default || c)
export const LazyLinaLogo = import('../../components/core/LinaLogo.vue' /* webpackChunkName: "components/core/LinaLogo" */).then(c => c.default || c)
export const LazyMaterialCard = import('../../components/core/MaterialCard.vue' /* webpackChunkName: "components/core/MaterialCard" */).then(c => c.default || c)
export const LazyUserLogin = import('../../components/core/UserLogin.vue' /* webpackChunkName: "components/core/UserLogin" */).then(c => c.default || c)
export const LazyUserRegister = import('../../components/core/UserRegister.vue' /* webpackChunkName: "components/core/UserRegister" */).then(c => c.default || c)
export const LazySelCols = import('../../components/utilities/SelCols.vue' /* webpackChunkName: "components/utilities/SelCols" */).then(c => c.default || c)
