import Vue from 'vue'
import Router from 'vue-router'
import { interopDefault } from './utils'
import scrollBehavior from './router.scrollBehavior.js'

const _c7ec75dc = () => interopDefault(import('../pages/login/index.vue' /* webpackChunkName: "pages/login/index" */))
const _411b05c2 = () => interopDefault(import('../pages/compras/facturas.vue' /* webpackChunkName: "pages/compras/facturas" */))
const _27524778 = () => interopDefault(import('../pages/compras/oc.vue' /* webpackChunkName: "pages/compras/oc" */))
const _0ebac994 = () => interopDefault(import('../pages/compras/provs.vue' /* webpackChunkName: "pages/compras/provs" */))
const _8d239f72 = () => interopDefault(import('../pages/compras/requisiciones.vue' /* webpackChunkName: "pages/compras/requisiciones" */))
const _c0f77d82 = () => interopDefault(import('../pages/crm/calendario.vue' /* webpackChunkName: "pages/crm/calendario" */))
const _2a25926a = () => interopDefault(import('../pages/crm/prospectos.vue' /* webpackChunkName: "pages/crm/prospectos" */))
const _67093a1e = () => interopDefault(import('../pages/crm/seguimiento.vue' /* webpackChunkName: "pages/crm/seguimiento" */))
const _16c84477 = () => interopDefault(import('../pages/inventario/bodegas.vue' /* webpackChunkName: "pages/inventario/bodegas" */))
const _46087ae4 = () => interopDefault(import('../pages/inventario/categorias.vue' /* webpackChunkName: "pages/inventario/categorias" */))
const _655e3510 = () => interopDefault(import('../pages/inventario/despachos.vue' /* webpackChunkName: "pages/inventario/despachos" */))
const _24e14740 = () => interopDefault(import('../pages/inventario/entradas.vue' /* webpackChunkName: "pages/inventario/entradas" */))
const _b01e4178 = () => interopDefault(import('../pages/inventario/manifiestos.vue' /* webpackChunkName: "pages/inventario/manifiestos" */))
const _aecc1802 = () => interopDefault(import('../pages/inventario/productos.vue' /* webpackChunkName: "pages/inventario/productos" */))
const _3d6773dc = () => interopDefault(import('../pages/inventario/um.vue' /* webpackChunkName: "pages/inventario/um" */))
const _3011fabf = () => interopDefault(import('../pages/linabi/favoritos.vue' /* webpackChunkName: "pages/linabi/favoritos" */))
const _6a0855f7 = () => interopDefault(import('../pages/linabi/genconsulta.vue' /* webpackChunkName: "pages/linabi/genconsulta" */))
const _39b622b6 = () => interopDefault(import('../pages/linabi/panel.vue' /* webpackChunkName: "pages/linabi/panel" */))
const _5ce7bfc0 = () => interopDefault(import('../pages/linabi/reportes.vue' /* webpackChunkName: "pages/linabi/reportes" */))
const _5b089438 = () => interopDefault(import('../pages/logistica/despachos.vue' /* webpackChunkName: "pages/logistica/despachos" */))
const _5d57d63a = () => interopDefault(import('../pages/logistica/reportes.vue' /* webpackChunkName: "pages/logistica/reportes" */))
const _aedf2c36 = () => interopDefault(import('../pages/logistica/ubicaciones.vue' /* webpackChunkName: "pages/logistica/ubicaciones" */))
const _645950f4 = () => interopDefault(import('../pages/logistica/vehiculos.vue' /* webpackChunkName: "pages/logistica/vehiculos" */))
const _29cc2968 = () => interopDefault(import('../pages/rrhh/cargos.vue' /* webpackChunkName: "pages/rrhh/cargos" */))
const _7e2fb799 = () => interopDefault(import('../pages/rrhh/consultas.vue' /* webpackChunkName: "pages/rrhh/consultas" */))
const _f6166cd6 = () => interopDefault(import('../pages/rrhh/personal.vue' /* webpackChunkName: "pages/rrhh/personal" */))
const _9bd47154 = () => interopDefault(import('../pages/rrhh/planilla.vue' /* webpackChunkName: "pages/rrhh/planilla" */))
const _83989222 = () => interopDefault(import('../pages/sistema/cias.vue' /* webpackChunkName: "pages/sistema/cias" */))
const _74352a59 = () => interopDefault(import('../pages/sistema/config.vue' /* webpackChunkName: "pages/sistema/config" */))
const _61a81cdc = () => interopDefault(import('../pages/sistema/usuarios.vue' /* webpackChunkName: "pages/sistema/usuarios" */))
const _f5992ff2 = () => interopDefault(import('../pages/ventas/clientes.vue' /* webpackChunkName: "pages/ventas/clientes" */))
const _246c4f49 = () => interopDefault(import('../pages/ventas/cotizaciones.vue' /* webpackChunkName: "pages/ventas/cotizaciones" */))
const _1460acc4 = () => interopDefault(import('../pages/ventas/devoluciones.vue' /* webpackChunkName: "pages/ventas/devoluciones" */))
const _d972356e = () => interopDefault(import('../pages/ventas/facturas.vue' /* webpackChunkName: "pages/ventas/facturas" */))
const _fbc49a00 = () => interopDefault(import('../pages/ventas/ncs.vue' /* webpackChunkName: "pages/ventas/ncs" */))
const _d08be320 = () => interopDefault(import('../pages/ventas/pedidos.vue' /* webpackChunkName: "pages/ventas/pedidos" */))
const _006450f6 = () => interopDefault(import('../pages/ventas/pos.vue' /* webpackChunkName: "pages/ventas/pos" */))
const _08c2c07c = () => interopDefault(import('../pages/ventas/utilidades.vue' /* webpackChunkName: "pages/ventas/utilidades" */))
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
    path: "/login",
    component: _c7ec75dc,
    name: "login"
  }, {
    path: "/compras/facturas",
    component: _411b05c2,
    name: "compras-facturas"
  }, {
    path: "/compras/oc",
    component: _27524778,
    name: "compras-oc"
  }, {
    path: "/compras/provs",
    component: _0ebac994,
    name: "compras-provs"
  }, {
    path: "/compras/requisiciones",
    component: _8d239f72,
    name: "compras-requisiciones"
  }, {
    path: "/crm/calendario",
    component: _c0f77d82,
    name: "crm-calendario"
  }, {
    path: "/crm/prospectos",
    component: _2a25926a,
    name: "crm-prospectos"
  }, {
    path: "/crm/seguimiento",
    component: _67093a1e,
    name: "crm-seguimiento"
  }, {
    path: "/inventario/bodegas",
    component: _16c84477,
    name: "inventario-bodegas"
  }, {
    path: "/inventario/categorias",
    component: _46087ae4,
    name: "inventario-categorias"
  }, {
    path: "/inventario/despachos",
    component: _655e3510,
    name: "inventario-despachos"
  }, {
    path: "/inventario/entradas",
    component: _24e14740,
    name: "inventario-entradas"
  }, {
    path: "/inventario/manifiestos",
    component: _b01e4178,
    name: "inventario-manifiestos"
  }, {
    path: "/inventario/productos",
    component: _aecc1802,
    name: "inventario-productos"
  }, {
    path: "/inventario/um",
    component: _3d6773dc,
    name: "inventario-um"
  }, {
    path: "/linabi/favoritos",
    component: _3011fabf,
    name: "linabi-favoritos"
  }, {
    path: "/linabi/genconsulta",
    component: _6a0855f7,
    name: "linabi-genconsulta"
  }, {
    path: "/linabi/panel",
    component: _39b622b6,
    name: "linabi-panel"
  }, {
    path: "/linabi/reportes",
    component: _5ce7bfc0,
    name: "linabi-reportes"
  }, {
    path: "/logistica/despachos",
    component: _5b089438,
    name: "logistica-despachos"
  }, {
    path: "/logistica/reportes",
    component: _5d57d63a,
    name: "logistica-reportes"
  }, {
    path: "/logistica/ubicaciones",
    component: _aedf2c36,
    name: "logistica-ubicaciones"
  }, {
    path: "/logistica/vehiculos",
    component: _645950f4,
    name: "logistica-vehiculos"
  }, {
    path: "/rrhh/cargos",
    component: _29cc2968,
    name: "rrhh-cargos"
  }, {
    path: "/rrhh/consultas",
    component: _7e2fb799,
    name: "rrhh-consultas"
  }, {
    path: "/rrhh/personal",
    component: _f6166cd6,
    name: "rrhh-personal"
  }, {
    path: "/rrhh/planilla",
    component: _9bd47154,
    name: "rrhh-planilla"
  }, {
    path: "/sistema/cias",
    component: _83989222,
    name: "sistema-cias"
  }, {
    path: "/sistema/config",
    component: _74352a59,
    name: "sistema-config"
  }, {
    path: "/sistema/usuarios",
    component: _61a81cdc,
    name: "sistema-usuarios"
  }, {
    path: "/ventas/clientes",
    component: _f5992ff2,
    name: "ventas-clientes"
  }, {
    path: "/ventas/cotizaciones",
    component: _246c4f49,
    name: "ventas-cotizaciones"
  }, {
    path: "/ventas/devoluciones",
    component: _1460acc4,
    name: "ventas-devoluciones"
  }, {
    path: "/ventas/facturas",
    component: _d972356e,
    name: "ventas-facturas"
  }, {
    path: "/ventas/ncs",
    component: _fbc49a00,
    name: "ventas-ncs"
  }, {
    path: "/ventas/pedidos",
    component: _d08be320,
    name: "ventas-pedidos"
  }, {
    path: "/ventas/pos",
    component: _006450f6,
    name: "ventas-pos"
  }, {
    path: "/ventas/utilidades",
    component: _08c2c07c,
    name: "ventas-utilidades"
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
