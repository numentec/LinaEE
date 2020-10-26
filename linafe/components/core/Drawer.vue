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
        <v-list-item to="/">
          <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title class="title">Inico</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-group
          v-for="item in items"
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
          <v-btn v-show="!is_expanded" icon class="secondary darken-2">
            <v-icon>mdi-logout-variant</v-icon>
          </v-btn>
          <v-btn v-show="is_expanded" rounded block class="secondary darken-2">
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
      items: [
        {
          icon: 'mdi-handshake-outline',
          title: 'CRM',
          items: [
            {
              icon: 'mdi-info',
              title: 'Prospectos',
              to: '/lina/crm/prospectos',
            },
            {
              icon: 'mdi-info',
              title: 'Seguimiento',
              to: '/lina/crm/seguimiento',
            },
            {
              icon: 'mdi-info',
              title: 'Calendario',
              to: '/lina/crm/calendario',
            },
          ],
        },
        {
          icon: 'mdi-storefront',
          title: 'Ventas',
          items: [
            {
              icon: 'mdi-info',
              title: 'Cotizaciones',
              to: '/lina/ventas/cotizaciones',
            },
            {
              icon: 'mdi-info',
              title: 'Pedidos',
              to: '/lina/ventas/pedidos',
            },
            {
              icon: 'mdi-info',
              title: 'Facturas',
              to: '/lina/ventas/facturas',
            },
            {
              icon: 'mdi-info',
              title: 'Notas de Crédito',
              to: '/lina/ventas/ncs',
            },
            {
              icon: 'mdi-info',
              title: 'Devoluciones',
              to: '/lina/ventas/devoluciones',
            },
            {
              icon: 'mdi-info',
              title: 'Punto de Venta',
              to: '/lina/ventas/pos',
            },
            {
              icon: 'mdi-info',
              title: 'Clientes',
              to: '/lina/ventas/clientes',
            },
            {
              icon: 'mdi-info',
              title: 'Utilidades',
              to: '/lina/ventas/utilidades',
            },
          ],
        },
        {
          icon: 'mdi-cart-plus',
          title: 'Compras',
          items: [
            {
              icon: 'mdi-info',
              title: 'Requisiciones',
              to: '/lina/inspire',
            },
            {
              icon: 'mdi-info',
              title: 'Ordenes de Compra',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Facturas',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Proveedores',
              to: '/',
            },
          ],
        },
        {
          icon: 'mdi-package-variant',
          title: 'Inventario',
          items: [
            {
              icon: 'mdi-info',
              title: 'Productos',
              to: '/inspire',
            },
            {
              icon: 'mdi-info',
              title: 'Entradas',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Despachos',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Categorías',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Unidades de Medida',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Bodegas',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Manifiestos',
              to: '/',
            },
          ],
        },
        {
          icon: 'mdi-account-cog',
          title: 'RR.HH',
          items: [
            {
              icon: 'mdi-info',
              title: 'Personal',
              to: '/inspire',
            },
            {
              icon: 'mdi-info',
              title: 'Cargos',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Planilla',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Consultas',
              to: '/',
            },
          ],
        },
        {
          icon: 'mdi-calculator-variant',
          title: 'Contabilidad',
          items: [
            {
              icon: 'mdi-info',
              title: 'Cobros a Cliente',
              to: '/inspire',
            },
            {
              icon: 'mdi-info',
              title: 'Pagos a Proveedor',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Asientos',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Caja',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Bancos',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Utilidades',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Reportes',
              to: '/',
            },
          ],
        },
        {
          icon: 'mdi-truck-fast',
          title: 'Logística',
          items: [
            {
              icon: 'mdi-info',
              title: 'Despachos',
              to: '/inspire',
            },
            {
              icon: 'mdi-info',
              title: 'Ubicaciones',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Vehículos',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Reportes',
              to: '/',
            },
          ],
        },
        {
          icon: 'mdi-finance',
          title: 'Lina Bi',
          items: [
            {
              icon: 'mdi-info',
              title: 'Panel',
              to: '/inspire',
            },
            {
              icon: 'mdi-info',
              title: 'Favoritos',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Generar Consulta',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Reportes',
              to: '/',
            },
          ],
        },
        {
          icon: 'mdi-application-cog',
          title: 'Sistema',
          items: [
            {
              icon: 'mdi-info',
              title: 'Empresas',
              to: '/lina/sistema/cias',
            },
            {
              icon: 'mdi-info',
              title: 'Usuarios',
              to: '/lina/sistema/usuarios',
            },
            {
              icon: 'mdi-info',
              title: 'Configuración',
              to: '/lina/sistema/config',
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
  },
}
</script>
