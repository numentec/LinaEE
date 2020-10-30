import Vue from 'vue'
import Router from 'vue-router'
import { interopDefault } from './utils'
import scrollBehavior from './router.scrollBehavior.js'

const _0dc5685a = () => interopDefault(import('../pages/directory.vue' /* webpackChunkName: "pages/directory" */))
const _5e9e1b7d = () => interopDefault(import('../pages/lina/index.vue' /* webpackChunkName: "pages/lina/index" */))
const _6b22c45a = () => interopDefault(import('../pages/webstore/index.vue' /* webpackChunkName: "pages/webstore/index" */))
const _ad33f3d2 = () => interopDefault(import('../pages/lina/login/index.vue' /* webpackChunkName: "pages/lina/login/index" */))
const _81c1d18c = () => interopDefault(import('../pages/lina/compras/facturas.vue' /* webpackChunkName: "pages/lina/compras/facturas" */))
const _fad15c5a = () => interopDefault(import('../pages/lina/compras/oc.vue' /* webpackChunkName: "pages/lina/compras/oc" */))
const _1ff2aefb = () => interopDefault(import('../pages/lina/compras/provs.vue' /* webpackChunkName: "pages/lina/compras/provs" */))
const _84b6a1e8 = () => interopDefault(import('../pages/lina/compras/requisiciones.vue' /* webpackChunkName: "pages/lina/compras/requisiciones" */))
const _6236a61a = () => interopDefault(import('../pages/lina/crm/calendario.vue' /* webpackChunkName: "pages/lina/crm/calendario" */))
const _a4c0c8b4 = () => interopDefault(import('../pages/lina/crm/prospectos.vue' /* webpackChunkName: "pages/lina/crm/prospectos" */))
const _0ab91eba = () => interopDefault(import('../pages/lina/crm/seguimiento.vue' /* webpackChunkName: "pages/lina/crm/seguimiento" */))
const _8492785c = () => interopDefault(import('../pages/lina/inventario/bodegas.vue' /* webpackChunkName: "pages/lina/inventario/bodegas" */))
const _4a3ef9a9 = () => interopDefault(import('../pages/lina/inventario/categorias.vue' /* webpackChunkName: "pages/lina/inventario/categorias" */))
const _729cfa13 = () => interopDefault(import('../pages/lina/inventario/despachos.vue' /* webpackChunkName: "pages/lina/inventario/despachos" */))
const _5bc2b345 = () => interopDefault(import('../pages/lina/inventario/entradas.vue' /* webpackChunkName: "pages/lina/inventario/entradas" */))
const _2a8a391f = () => interopDefault(import('../pages/lina/inventario/manifiestos.vue' /* webpackChunkName: "pages/lina/inventario/manifiestos" */))
const _4de6089a = () => interopDefault(import('../pages/lina/inventario/productos.vue' /* webpackChunkName: "pages/lina/inventario/productos" */))
const _64b787a1 = () => interopDefault(import('../pages/lina/inventario/um.vue' /* webpackChunkName: "pages/lina/inventario/um" */))
const _0fbe94da = () => interopDefault(import('../pages/lina/linabi/favoritos.vue' /* webpackChunkName: "pages/lina/linabi/favoritos" */))
const _10f6d552 = () => interopDefault(import('../pages/lina/linabi/genconsulta.vue' /* webpackChunkName: "pages/lina/linabi/genconsulta" */))
const _503bfb5e = () => interopDefault(import('../pages/lina/linabi/panel.vue' /* webpackChunkName: "pages/lina/linabi/panel" */))
const _652656a5 = () => interopDefault(import('../pages/lina/linabi/reportes.vue' /* webpackChunkName: "pages/lina/linabi/reportes" */))
const _095d21e9 = () => interopDefault(import('../pages/lina/logistica/despachos.vue' /* webpackChunkName: "pages/lina/logistica/despachos" */))
const _04465595 = () => interopDefault(import('../pages/lina/logistica/reportes.vue' /* webpackChunkName: "pages/lina/logistica/reportes" */))
const _a6722eac = () => interopDefault(import('../pages/lina/logistica/ubicaciones.vue' /* webpackChunkName: "pages/lina/logistica/ubicaciones" */))
const _04b4c38b = () => interopDefault(import('../pages/lina/logistica/vehiculos.vue' /* webpackChunkName: "pages/lina/logistica/vehiculos" */))
const _0f13a75e = () => interopDefault(import('../pages/lina/rrhh/cargos.vue' /* webpackChunkName: "pages/lina/rrhh/cargos" */))
const _40e21c74 = () => interopDefault(import('../pages/lina/rrhh/consultas.vue' /* webpackChunkName: "pages/lina/rrhh/consultas" */))
const _a776454c = () => interopDefault(import('../pages/lina/rrhh/personal.vue' /* webpackChunkName: "pages/lina/rrhh/personal" */))
const _4d3449ca = () => interopDefault(import('../pages/lina/rrhh/planilla.vue' /* webpackChunkName: "pages/lina/rrhh/planilla" */))
const _5c5f968a = () => interopDefault(import('../pages/lina/sistema/cias.vue' /* webpackChunkName: "pages/lina/sistema/cias" */))
const _36e78f34 = () => interopDefault(import('../pages/lina/sistema/config.vue' /* webpackChunkName: "pages/lina/sistema/config" */))
const _4154b6f7 = () => interopDefault(import('../pages/lina/sistema/usuarios.vue' /* webpackChunkName: "pages/lina/sistema/usuarios" */))
const _18cd9e8c = () => interopDefault(import('../pages/lina/ventas/clientes.vue' /* webpackChunkName: "pages/lina/ventas/clientes" */))
const _5b4dbb4e = () => interopDefault(import('../pages/lina/ventas/cotizaciones.vue' /* webpackChunkName: "pages/lina/ventas/cotizaciones" */))
const _4b4218c9 = () => interopDefault(import('../pages/lina/ventas/devoluciones.vue' /* webpackChunkName: "pages/lina/ventas/devoluciones" */))
const _26e11bce = () => interopDefault(import('../pages/lina/ventas/facturas.vue' /* webpackChunkName: "pages/lina/ventas/facturas" */))
const _453a854a = () => interopDefault(import('../pages/lina/ventas/ncs.vue' /* webpackChunkName: "pages/lina/ventas/ncs" */))
const _5a6c734b = () => interopDefault(import('../pages/lina/ventas/pedidos.vue' /* webpackChunkName: "pages/lina/ventas/pedidos" */))
const _5ba95b51 = () => interopDefault(import('../pages/lina/ventas/pos.vue' /* webpackChunkName: "pages/lina/ventas/pos" */))
const _1ea969c1 = () => interopDefault(import('../pages/lina/ventas/utilidades.vue' /* webpackChunkName: "pages/lina/ventas/utilidades" */))
const _ea611a90 = () => interopDefault(import('../pages/index.vue' /* webpackChunkName: "pages/index" */))

// TODO: remove in Nuxt 3
const emptyFn = () => {}
const originalPush = Router.prototype.push
Router.prototype.push = function push (location, onComplete = emptyFn, onAbort) {
  return originalPush.call(this, location, onComplete, onAbort)
}

Vue.use(Router)

export const routerOptions = {
  mode: 'history',
  base: decodeURI('/'),
  linkActiveClass: 'nuxt-link-active',
  linkExactActiveClass: 'nuxt-link-exact-active',
  scrollBehavior,

  routes: [{
    path: "/directory",
    component: _0dc5685a,
    name: "directory"
  }, {
    path: "/lina",
    component: _5e9e1b7d,
    name: "lina"
  }, {
    path: "/webstore",
    component: _6b22c45a,
    name: "webstore"
  }, {
    path: "/lina/login",
    component: _ad33f3d2,
    name: "lina-login"
  }, {
    path: "/lina/compras/facturas",
    component: _81c1d18c,
    name: "lina-compras-facturas"
  }, {
    path: "/lina/compras/oc",
    component: _fad15c5a,
    name: "lina-compras-oc"
  }, {
    path: "/lina/compras/provs",
    component: _1ff2aefb,
    name: "lina-compras-provs"
  }, {
    path: "/lina/compras/requisiciones",
    component: _84b6a1e8,
    name: "lina-compras-requisiciones"
  }, {
    path: "/lina/crm/calendario",
    component: _6236a61a,
    name: "lina-crm-calendario"
  }, {
    path: "/lina/crm/prospectos",
    component: _a4c0c8b4,
    name: "lina-crm-prospectos"
  }, {
    path: "/lina/crm/seguimiento",
    component: _0ab91eba,
    name: "lina-crm-seguimiento"
  }, {
    path: "/lina/inventario/bodegas",
    component: _8492785c,
    name: "lina-inventario-bodegas"
  }, {
    path: "/lina/inventario/categorias",
    component: _4a3ef9a9,
    name: "lina-inventario-categorias"
  }, {
    path: "/lina/inventario/despachos",
    component: _729cfa13,
    name: "lina-inventario-despachos"
  }, {
    path: "/lina/inventario/entradas",
    component: _5bc2b345,
    name: "lina-inventario-entradas"
  }, {
    path: "/lina/inventario/manifiestos",
    component: _2a8a391f,
    name: "lina-inventario-manifiestos"
  }, {
    path: "/lina/inventario/productos",
    component: _4de6089a,
    name: "lina-inventario-productos"
  }, {
    path: "/lina/inventario/um",
    component: _64b787a1,
    name: "lina-inventario-um"
  }, {
    path: "/lina/linabi/favoritos",
    component: _0fbe94da,
    name: "lina-linabi-favoritos"
  }, {
    path: "/lina/linabi/genconsulta",
    component: _10f6d552,
    name: "lina-linabi-genconsulta"
  }, {
    path: "/lina/linabi/panel",
    component: _503bfb5e,
    name: "lina-linabi-panel"
  }, {
    path: "/lina/linabi/reportes",
    component: _652656a5,
    name: "lina-linabi-reportes"
  }, {
    path: "/lina/logistica/despachos",
    component: _095d21e9,
    name: "lina-logistica-despachos"
  }, {
    path: "/lina/logistica/reportes",
    component: _04465595,
    name: "lina-logistica-reportes"
  }, {
    path: "/lina/logistica/ubicaciones",
    component: _a6722eac,
    name: "lina-logistica-ubicaciones"
  }, {
    path: "/lina/logistica/vehiculos",
    component: _04b4c38b,
    name: "lina-logistica-vehiculos"
  }, {
    path: "/lina/rrhh/cargos",
    component: _0f13a75e,
    name: "lina-rrhh-cargos"
  }, {
    path: "/lina/rrhh/consultas",
    component: _40e21c74,
    name: "lina-rrhh-consultas"
  }, {
    path: "/lina/rrhh/personal",
    component: _a776454c,
    name: "lina-rrhh-personal"
  }, {
    path: "/lina/rrhh/planilla",
    component: _4d3449ca,
    name: "lina-rrhh-planilla"
  }, {
    path: "/lina/sistema/cias",
    component: _5c5f968a,
    name: "lina-sistema-cias"
  }, {
    path: "/lina/sistema/config",
    component: _36e78f34,
    name: "lina-sistema-config"
  }, {
    path: "/lina/sistema/usuarios",
    component: _4154b6f7,
    name: "lina-sistema-usuarios"
  }, {
    path: "/lina/ventas/clientes",
    component: _18cd9e8c,
    name: "lina-ventas-clientes"
  }, {
    path: "/lina/ventas/cotizaciones",
    component: _5b4dbb4e,
    name: "lina-ventas-cotizaciones"
  }, {
    path: "/lina/ventas/devoluciones",
    component: _4b4218c9,
    name: "lina-ventas-devoluciones"
  }, {
    path: "/lina/ventas/facturas",
    component: _26e11bce,
    name: "lina-ventas-facturas"
  }, {
    path: "/lina/ventas/ncs",
    component: _453a854a,
    name: "lina-ventas-ncs"
  }, {
    path: "/lina/ventas/pedidos",
    component: _5a6c734b,
    name: "lina-ventas-pedidos"
  }, {
    path: "/lina/ventas/pos",
    component: _5ba95b51,
    name: "lina-ventas-pos"
  }, {
    path: "/lina/ventas/utilidades",
    component: _1ea969c1,
    name: "lina-ventas-utilidades"
  }, {
    path: "/",
    component: _ea611a90,
    name: "index"
  }],

  fallback: false
}

export function createRouter () {
  return new Router(routerOptions)
}
