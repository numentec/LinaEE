// Sort by integer and fractional parts of type "int / frac"
function sortIntFrac(val1, val2) {
  // Handling null values
  if (!val1 && val2) return -1
  if (!val1 && !val2) return 0
  if (val1 && !val2) return 1

  // If not null values
  const [int1 = '0', frac1 = '0'] = val1.split('/')
  const [int2 = '0', frac2 = '0'] = val2.split('/')

  const v1 = Number(int1.trim()) + Number(frac1.trim()) / 100
  const v2 = Number(int2.trim()) + Number(frac2.trim()) / 100

  if (v1 < v2) return -1
  if (v1 === v2) return 0
  if (v1 > v2) return 1
}

export const modulos = [
  {
    name: 'crm',
    icon: 'mdi-handshake-outline',
    title: 'CRM',
    perm: 'core.acc_crm',
    items: [
      {
        icon: 'mdi-info',
        title: 'Prospectos',
        to: '/crm/prospectos',
      },
      {
        icon: 'mdi-info',
        title: 'Seguimiento',
        to: '/crm/seguimiento',
      },
      {
        icon: 'mdi-info',
        title: 'Calendario',
        to: '/crm/calendario',
      },
    ],
  },
  {
    name: 'ventas',
    icon: 'mdi-storefront',
    title: 'Ventas',
    perm: 'core.acc_sales',
    items: [
      {
        icon: 'mdi-info',
        title: 'Cotizaciones',
        to: '/ventas/cotizaciones',
      },
      {
        icon: 'mdi-info',
        title: 'Pedidos',
        to: '/ventas/pedidos',
      },
      {
        icon: 'mdi-info',
        title: 'Facturas',
        to: '/ventas/facturas',
      },
      {
        icon: 'mdi-info',
        title: 'Notas de Crédito',
        to: '/ventas/ncs',
      },
      {
        icon: 'mdi-info',
        title: 'Devoluciones',
        to: '/ventas/devoluciones',
      },
      {
        icon: 'mdi-info',
        title: 'Punto de Venta',
        to: '/ventas/pos',
      },
      {
        icon: 'mdi-info',
        title: 'Clientes',
        to: '/ventas/clientes',
      },
      {
        icon: 'mdi-info',
        title: 'Utilidades',
        to: '/ventas/utilidades',
      },
    ],
  },
  {
    name: 'compras',
    icon: 'mdi-cart-plus',
    title: 'Compras',
    perm: 'core.acc_purchase',
    items: [
      {
        icon: 'mdi-info',
        title: 'Requisiciones',
        to: '/compras/requisiciones',
      },
      {
        icon: 'mdi-info',
        title: 'Ordenes de Compra',
        to: '/compras/oc',
      },
      {
        icon: 'mdi-info',
        title: 'Facturas',
        to: '/compras/facturas',
      },
      {
        icon: 'mdi-info',
        title: 'Proveedores',
        to: '/compras/provs',
      },
    ],
  },
  {
    name: 'inv',
    icon: 'mdi-package-variant',
    title: 'Inventario',
    perm: 'core.acc_inv',
    items: [
      {
        icon: 'mdi-info',
        title: 'Productos',
        to: '/inventario/productos',
      },
      {
        icon: 'mdi-info',
        title: 'Entradas',
        to: '/inventario/entradas',
      },
      {
        icon: 'mdi-info',
        title: 'Despachos',
        to: '/inventario/despachos',
      },
      {
        icon: 'mdi-info',
        title: 'Categorías',
        to: '/inventario/categorias',
      },
      {
        icon: 'mdi-info',
        title: 'Unidades de Medida',
        to: '/inventario/um',
      },
      {
        icon: 'mdi-info',
        title: 'Bodegas',
        to: '/inventario/bodegas',
      },
      {
        icon: 'mdi-info',
        title: 'Manifiestos',
        to: '/inventario/manifiestos',
      },
    ],
  },
  {
    name: 'wms',
    icon: 'mdi-warehouse',
    title: 'WMS',
    perm: 'core.acc_wms',
    items: [
      {
        icon: 'mdi-info',
        title: 'Herramientas',
        to: '/wms/tools',
      },
    ],
  },
  {
    name: 'rrhh',
    icon: 'mdi-account-cog',
    title: 'RR.HH',
    perm: 'core.acc_hr',
    items: [
      {
        icon: 'mdi-info',
        title: 'Personal',
        to: '/rrhh/personal',
      },
      {
        icon: 'mdi-info',
        title: 'Cargos',
        to: '/rrhh/cargos',
      },
      {
        icon: 'mdi-info',
        title: 'Planilla',
        to: '/rrhh/planilla',
      },
      {
        icon: 'mdi-info',
        title: 'Consultas',
        to: '/rrhh/consultas',
      },
    ],
  },
  {
    name: 'conta',
    icon: 'mdi-calculator-variant',
    title: 'Contabilidad',
    perm: 'core.acc_accounting',
    items: [
      {
        icon: 'mdi-info',
        title: 'Cobros a Cliente',
        to: '/conta/cobroscli',
      },
      {
        icon: 'mdi-info',
        title: 'Pagos a Proveedor',
        to: '/conta/pagosprov',
      },
      {
        icon: 'mdi-info',
        title: 'Asientos',
        to: '/conta/asientos',
      },
      {
        icon: 'mdi-info',
        title: 'Caja',
        to: '/conta/caja',
      },
      {
        icon: 'mdi-info',
        title: 'Bancos',
        to: '/conta/bancos',
      },
      {
        icon: 'mdi-info',
        title: 'Utilidades',
        to: '/conta/utilidades',
      },
      {
        icon: 'mdi-info',
        title: 'Reportes',
        to: '/conta/reportes',
      },
    ],
  },
  {
    name: 'logistica',
    icon: 'mdi-truck-fast',
    title: 'Logística',
    perm: 'core.acc_logistics',
    items: [
      {
        icon: 'mdi-info',
        title: 'Despachos',
        to: '/logistica/despachos',
      },
      {
        icon: 'mdi-info',
        title: 'Ubicaciones',
        to: '/logistica/ubicaciones',
      },
      {
        icon: 'mdi-info',
        title: 'Vehículos',
        to: '/logistica/vehiculos',
      },
      {
        icon: 'mdi-info',
        title: 'Reportes',
        to: '/logistica/reportes',
      },
    ],
  },
  {
    name: 'linabi',
    icon: 'mdi-finance',
    title: 'Lina Bi',
    perm: 'core.acc_linabi',
    items: [
      {
        icon: 'mdi-info',
        title: 'Panel',
        to: '/linabi/',
      },
      {
        icon: 'mdi-info',
        title: 'Favoritos',
        to: '/linabi/favoritos',
      },
      {
        icon: 'mdi-info',
        title: 'Consultas',
        to: '/linabi/consultas',
      },
      {
        icon: 'mdi-info',
        title: 'Reportes',
        to: '/linabi/reportes',
      },
    ],
  },
  {
    name: 'config',
    icon: 'mdi-application-cog',
    title: 'Ajustes',
    perm: 'core.acc_config',
    items: [
      {
        icon: 'mdi-info',
        title: 'Empresas',
        to: '/sistema/cias',
      },
      {
        icon: 'mdi-info',
        title: 'Usuarios',
        to: '/sistema/usuarios',
      },
      {
        icon: 'mdi-info',
        title: 'Opciones',
        to: '/sistema/config',
      },
    ],
  },
]

export function selFunction(func) {
  const funcs = {
    sortIntFrac,
  }
  return funcs[func] ?? undefined
}
