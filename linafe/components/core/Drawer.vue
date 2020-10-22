<template>
  <div @mouseover="setIsExpanded(true)" @mouseout="setIsExpanded(!is_mini)">
    <v-navigation-drawer
      v-model="drawer"
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
              to: '/inspire',
            },
            {
              icon: 'mdi-info',
              title: 'Seguimiento',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Calendario',
              to: '/',
            },
          ],
        },
        {
          icon: 'mdi-storefront',
          title: 'Ventas',
          items: [
            {
              icon: 'mdi-info',
              title: 'Cotización',
              to: '/inspire',
            },
            {
              icon: 'mdi-info',
              title: 'Pedido',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Factura',
              to: '/inspire',
            },
            {
              icon: 'mdi-info',
              title: 'Notas de Crédito',
              to: '/inspire',
            },
            {
              icon: 'mdi-info',
              title: 'Punto de Venta',
              to: '/inspire',
            },
            {
              icon: 'mdi-info',
              title: 'Clientes',
              to: '/inspire',
            },
            {
              icon: 'mdi-info',
              title: 'Utilidades',
              to: '/inspire',
            },
          ],
        },
        {
          icon: 'mdi-cart-plus',
          title: 'Compras',
          items: [
            {
              icon: 'mdi-info',
              title: 'Requisición',
              to: '/inspire',
            },
            {
              icon: 'mdi-info',
              title: 'Orden de Compra',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Factura',
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
              title: 'Entrada',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Despacho',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Categorías',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Unidad de Medida',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Bodegas',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Manifiesto',
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
              title: 'Cobro a Cliente',
              to: '/inspire',
            },
            {
              icon: 'mdi-info',
              title: 'Pago a Proveedor',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Asiento',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Caja',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Banco',
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
              title: 'Despacho',
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
              to: '/inspire',
            },
            {
              icon: 'mdi-info',
              title: 'Usuarios',
              to: '/',
            },
            {
              icon: 'mdi-info',
              title: 'Configuración',
              to: '/',
            },
          ],
        },
      ],
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
