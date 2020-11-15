<template>
  <div @mouseover="setIsExpanded(true)" @mouseout="setIsExpanded(!is_mini)">
    <v-navigation-drawer
      v-model="drawer_mode"
      permanent
      :mini-variant="is_mini"
      :expand-on-hover="is_mini"
      clipped
      fixed
      app
      dark
      class="primary darken-4"
    >
      <v-list shaped>
        <v-list-item nuxt to="/">
          <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title class="title">Inico</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-group
          v-for="item in items"
          v-show="perms[item.perm]"
          :key="item.title"
          :prepend-icon="item.icon"
          no-action
        >
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title v-text="item.title" />
            </v-list-item-content>
          </template>
          <v-list-item
            v-for="subitem in item.items"
            :key="subitem.title"
            nuxt
            :to="subitem.to"
            router
            exact
          >
            <v-list-item-content>
              <v-list-item-title v-text="subitem.title" />
            </v-list-item-content>
          </v-list-item>
        </v-list-group>
      </v-list>
      <template v-slot:append>
        <div class="pa-2">
          <v-btn
            v-show="!is_expanded"
            icon
            class="secondary darken-2"
            @click="userLogout"
          >
            <v-icon>mdi-logout-variant</v-icon>
          </v-btn>
          <v-btn
            v-show="is_expanded"
            rounded
            block
            class="secondary darken-2"
            @click="userLogout"
          >
            Logout
            <v-icon>mdi-logout-variant</v-icon>
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
  name: 'CoreDrawer',

  data() {
    return {
      perms: this.$auth.user.perms,
      items: [
        {
          icon: 'mdi-handshake-outline',
          title: 'CRM',
          perm: 'core.view_crm_module',
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
          icon: 'mdi-storefront',
          title: 'Ventas',
          perm: 'core.view_sales_module',
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
          icon: 'mdi-cart-plus',
          title: 'Compras',
          perm: 'core.view_purchase_module',
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
          icon: 'mdi-package-variant',
          title: 'Inventario',
          perm: 'core.view_inv_module',
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
          icon: 'mdi-account-cog',
          title: 'RR.HH',
          perm: 'core.view_hr_module',
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
          icon: 'mdi-calculator-variant',
          title: 'Contabilidad',
          perm: 'core.view_accounting_module',
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
          icon: 'mdi-truck-fast',
          title: 'Logística',
          perm: 'core.view_logistics_module',
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
          icon: 'mdi-finance',
          title: 'Lina Bi',
          perm: 'core.view_linabi_module',
          items: [
            {
              icon: 'mdi-info',
              title: 'Panel',
              to: '/linabi/panel',
            },
            {
              icon: 'mdi-info',
              title: 'Favoritos',
              to: '/linabi/favoritos',
            },
            {
              icon: 'mdi-info',
              title: 'Generar Consulta',
              to: '/linabi/genconsulta',
            },
            {
              icon: 'mdi-info',
              title: 'Reportes',
              to: '/linabi/reportes',
            },
          ],
        },
        {
          icon: 'mdi-application-cog',
          title: 'Sistema',
          perm: 'core.view_sys_module',
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
              title: 'Configuración',
              to: '/sistema/config',
            },
          ],
        },
      ],
      drawer_mode: null,
    }
  },

  computed: {
    ...mapState('core', {
      drawer: (state) => state.drawer,
      is_mini: (state) => state.is_mini,
      is_expanded: (state) => state.is_expanded,
    }),
  },

  methods: {
    ...mapActions('core', ['SetDrawer', 'setIsExpanded']),
    ...mapActions('sistema', ['userLogout']),
  },
}
</script>
