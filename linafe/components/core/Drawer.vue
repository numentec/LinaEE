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
        <v-list-item to="/lina">
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
              to: '/lina/compras/requisiciones',
            },
            {
              icon: 'mdi-info',
              title: 'Ordenes de Compra',
              to: '/lina/compras/oc',
            },
            {
              icon: 'mdi-info',
              title: 'Facturas',
              to: '/lina/compras/facturas',
            },
            {
              icon: 'mdi-info',
              title: 'Proveedores',
              to: '/lina/compras/provs',
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
              to: '/lina/inventario/productos',
            },
            {
              icon: 'mdi-info',
              title: 'Entradas',
              to: '/lina/inventario/entradas',
            },
            {
              icon: 'mdi-info',
              title: 'Despachos',
              to: '/lina/inventario/despachos',
            },
            {
              icon: 'mdi-info',
              title: 'Categorías',
              to: '/lina/inventario/categorias',
            },
            {
              icon: 'mdi-info',
              title: 'Unidades de Medida',
              to: '/lina/inventario/um',
            },
            {
              icon: 'mdi-info',
              title: 'Bodegas',
              to: '/lina/inventario/bodegas',
            },
            {
              icon: 'mdi-info',
              title: 'Manifiestos',
              to: '/lina/inventario/manifiestos',
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
              to: '/lina/rrhh/personal',
            },
            {
              icon: 'mdi-info',
              title: 'Cargos',
              to: '/lina/rrhh/cargos',
            },
            {
              icon: 'mdi-info',
              title: 'Planilla',
              to: '/lina/rrhh/planilla',
            },
            {
              icon: 'mdi-info',
              title: 'Consultas',
              to: '/lina/rrhh/consultas',
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
              to: '/lina/conta/cobroscli',
            },
            {
              icon: 'mdi-info',
              title: 'Pagos a Proveedor',
              to: '/lina/conta/pagosprov',
            },
            {
              icon: 'mdi-info',
              title: 'Asientos',
              to: '/lina/conta/asientos',
            },
            {
              icon: 'mdi-info',
              title: 'Caja',
              to: '/lina/conta/caja',
            },
            {
              icon: 'mdi-info',
              title: 'Bancos',
              to: '/lina/conta/bancos',
            },
            {
              icon: 'mdi-info',
              title: 'Utilidades',
              to: '/lina/conta/utilidades',
            },
            {
              icon: 'mdi-info',
              title: 'Reportes',
              to: '/lina/conta/reportes',
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
              to: '/lina/logistica/despachos',
            },
            {
              icon: 'mdi-info',
              title: 'Ubicaciones',
              to: '/lina/logistica/ubicaciones',
            },
            {
              icon: 'mdi-info',
              title: 'Vehículos',
              to: '/lina/logistica/vehiculos',
            },
            {
              icon: 'mdi-info',
              title: 'Reportes',
              to: '/lina/logistica/reportes',
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
              to: '/lina/linabi/panel',
            },
            {
              icon: 'mdi-info',
              title: 'Favoritos',
              to: '/lina/linabi/favoritos',
            },
            {
              icon: 'mdi-info',
              title: 'Generar Consulta',
              to: '/lina/linabi/genconsulta',
            },
            {
              icon: 'mdi-info',
              title: 'Reportes',
              to: '/lina/linabi/reportes',
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
