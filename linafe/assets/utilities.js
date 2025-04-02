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
        perm: 'core.acc_crm',
      },
      {
        icon: 'mdi-info',
        title: 'Seguimiento',
        to: '/crm/seguimiento',
        perm: 'core.acc_crm',
      },
      {
        icon: 'mdi-info',
        title: 'Calendario',
        to: '/crm/calendario',
        perm: 'core.acc_crm',
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
        perm: 'core.acc_sales',
      },
      {
        icon: 'mdi-info',
        title: 'Pedidos',
        to: '/ventas/pedidos',
        perm: 'core.acc_sales',
      },
      {
        icon: 'mdi-info',
        title: 'Facturas',
        to: '/ventas/facturas',
        perm: 'core.acc_sales',
      },
      {
        icon: 'mdi-info',
        title: 'Notas de Crédito',
        to: '/ventas/ncs',
        perm: 'core.acc_sales',
      },
      {
        icon: 'mdi-info',
        title: 'Devoluciones',
        to: '/ventas/devoluciones',
        perm: 'core.acc_sales',
      },
      {
        icon: 'mdi-info',
        title: 'Punto de Venta',
        to: '/ventas/pos',
        perm: 'core.acc_sales',
      },
      {
        icon: 'mdi-info',
        title: 'Clientes',
        to: '/ventas/clientes',
        perm: 'core.acc_sales',
      },
      {
        icon: 'mdi-info',
        title: 'Utilidades',
        to: '/ventas/utilidades',
        perm: 'core.acc_sales',
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
        perm: 'core.acc_purchase',
      },
      {
        icon: 'mdi-info',
        title: 'Ordenes de Compra',
        to: '/compras/oc',
        perm: 'core.acc_purchase',
      },
      {
        icon: 'mdi-info',
        title: 'Facturas',
        to: '/compras/facturas',
        perm: 'core.acc_purchase',
      },
      {
        icon: 'mdi-info',
        title: 'Proveedores',
        to: '/compras/provs',
        perm: 'core.acc_purchase',
      },
    ],
  },
  {
    name: 'shoppingcart',
    icon: 'mdi-cart-variant',
    title: 'Shopping',
    perm: 'core.acc_crm',
    items: [
      {
        icon: 'mdi-format-list-text',
        title: 'Inicio',
        // to: '/shoppingcart/',
        to: '/shoppingcart/categories/departments?category=Departments',
        perm: 'core.acc_crm',
      },
      {
        icon: 'mdi-cart-arrow-right',
        title: 'Go to cart',
        to: '/shoppingcart/cart',
        perm: 'core.acc_crm',
      },
      {
        icon: 'mdi-format-list-text',
        title: 'Orders',
        to: '/shoppingcart/ordersview',
        perm: 'core.acc_crm',
      },
      {
        icon: 'mdi-cog-outline',
        title: 'Tools',
        to: '/shoppingcart/tools',
        perm: 'core.acc_crm',
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
        perm: 'core.acc_inv',
      },
      {
        icon: 'mdi-info',
        title: 'Entradas',
        to: '/inventario/entradas',
        perm: 'core.acc_inv',
      },
      {
        icon: 'mdi-info',
        title: 'Despachos',
        to: '/inventario/despachos',
        perm: 'core.acc_inv',
      },
      {
        icon: 'mdi-info',
        title: 'Categorías',
        to: '/inventario/categorias',
        perm: 'core.acc_inv',
      },
      {
        icon: 'mdi-info',
        title: 'Unidades de Medida',
        to: '/inventario/um',
        perm: 'core.acc_inv',
      },
      {
        icon: 'mdi-info',
        title: 'Bodegas',
        to: '/inventario/bodegas',
        perm: 'core.acc_inv',
      },
      {
        icon: 'mdi-info',
        title: 'Manifiestos',
        to: '/inventario/manifiestos',
        perm: 'core.acc_inv',
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
        perm: 'core.acc_wms',
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
        perm: 'core.acc_hr',
      },
      {
        icon: 'mdi-info',
        title: 'Cargos',
        to: '/rrhh/cargos',
        perm: 'core.acc_hr',
      },
      {
        icon: 'mdi-info',
        title: 'Planilla',
        to: '/rrhh/planilla',
        perm: 'core.acc_hr',
      },
      {
        icon: 'mdi-info',
        title: 'Consultas',
        to: '/rrhh/consultas',
        perm: 'core.acc_hr',
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
        perm: 'core.acc_accounting',
      },
      {
        icon: 'mdi-info',
        title: 'Pagos a Proveedor',
        to: '/conta/pagosprov',
        perm: 'core.acc_accounting',
      },
      {
        icon: 'mdi-info',
        title: 'Asientos',
        to: '/conta/asientos',
        perm: 'core.acc_accounting',
      },
      {
        icon: 'mdi-info',
        title: 'Caja',
        to: '/conta/caja',
        perm: 'core.acc_accounting',
      },
      {
        icon: 'mdi-info',
        title: 'Bancos',
        to: '/conta/bancos',
        perm: 'core.acc_accounting',
      },
      {
        icon: 'mdi-info',
        title: 'Utilidades',
        to: '/conta/utilidades',
        perm: 'core.acc_accounting',
      },
      {
        icon: 'mdi-info',
        title: 'Reportes',
        to: '/conta/reportes',
        perm: 'core.acc_accounting',
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
        perm: 'core.acc_logistics',
      },
      {
        icon: 'mdi-info',
        title: 'Ubicaciones',
        to: '/logistica/ubicaciones',
        perm: 'core.acc_logistics',
      },
      {
        icon: 'mdi-info',
        title: 'Vehículos',
        to: '/logistica/vehiculos',
        perm: 'core.acc_logistics',
      },
      {
        icon: 'mdi-info',
        title: 'Reportes',
        to: '/logistica/reportes',
        perm: 'core.acc_logistics',
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
        perm: 'core.acc_linabi_panel',
      },
      {
        icon: 'mdi-info',
        title: 'Favoritos',
        to: '/linabi/favoritos',
        perm: 'core.acc_linabi',
      },
      {
        icon: 'mdi-info',
        title: 'Consultas',
        to: '/linabi/consultas',
        perm: 'core.acc_linabi',
      },
      {
        icon: 'mdi-info',
        title: 'Reportes',
        to: '/linabi/reportes',
        perm: 'core.acc_linabi',
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
        perm: 'core.acc_config',
      },
      {
        icon: 'mdi-info',
        title: 'Usuarios',
        to: '/sistema/usuarios',
        perm: 'core.acc_config',
      },
      {
        icon: 'mdi-info',
        title: 'Opciones',
        to: '/sistema/config',
        perm: 'core.acc_config',
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
