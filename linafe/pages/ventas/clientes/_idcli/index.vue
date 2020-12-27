<template>
  <v-card class="mx-auto mt-10">
    <v-toolbar color="secondary" dense dark fixed>
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item v-for="(item, i) in menu_items" :key="i" link>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      <v-toolbar-title>Cliente</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-app-bar-nav-icon @click.stop="showSearch">
        <v-icon v-if="showsearch">mdi-arrow-collapse-horizontal</v-icon>
        <v-icon v-else>mdi-magnify</v-icon>
      </v-app-bar-nav-icon>
      <template v-slot:extension>
        <v-tabs v-model="tab" grow dense dark>
          <v-tab key="1">Pag. 1</v-tab>
          <v-tab key="2">Pag. 2</v-tab>
          <v-tab key="3">Pag. 3</v-tab>
        </v-tabs>
      </template>
    </v-toolbar>
    <v-row>
      <v-col class="shrink" :cols="cols_mainbody">
        <v-form id="curform" ref="curform" @submit.prevent="submit">
          <v-tabs-items v-model="tab">
            <v-tab-item key="1" class="px-2" :eager="true">
              <v-card class="mx-auto mb-0" flat tile>
                <v-row>
                  <v-col align="center" justify="center" cols="12" md="4">
                    <v-img
                      lazy-src="https://picsum.photos/id/11/10/6"
                      max-height="150"
                      max-width="150"
                      src="https://picsum.photos/id/11/500/300"
                    ></v-img>
                  </v-col>
                  <v-col cols="12" md="8">
                    <v-row>
                      <v-col cols="8">
                        <v-text-field
                          v-model="curCli.nombre"
                          name="nombre"
                          label="Nombre"
                          dense
                        ></v-text-field>
                      </v-col>
                      <v-col cols="4">
                        <v-select
                          v-model="curCli.tipo"
                          name="tipo"
                          :items="items_persona"
                          item-text="name"
                          item-value="id"
                          label="Tipo de Personería"
                          dense
                        >
                        </v-select>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col cols="8">
                        <v-text-field
                          v-model="curCli.ruc"
                          name="ruc"
                          label="RUC"
                          dense
                        ></v-text-field>
                      </v-col>
                      <v-col cols="4">
                        <v-text-field
                          v-model="curCli.dv"
                          name="dv"
                          label="DV"
                          dense
                        ></v-text-field>
                      </v-col>
                    </v-row>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="4">
                    <v-text-field
                      v-model="curCli.tel1"
                      name="tel1"
                      label="Tel1"
                      dense
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-text-field
                      v-model="curCli.tel2"
                      name="tel2"
                      label="Tel2"
                      dense
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-text-field
                      v-model="curCli.tel3"
                      name="tel3"
                      label="Tel3"
                      dense
                    ></v-text-field>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="4">
                    <v-text-field
                      v-model="curCli.email"
                      name="email"
                      label="E-mail"
                      dense
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="8">
                    <v-textarea
                      v-model="curCli.direccion"
                      name="direccion"
                      label="Dirección"
                      rows="2"
                      dense
                    ></v-textarea>
                  </v-col>
                </v-row>
              </v-card>
            </v-tab-item>
            <v-tab-item key="2" :eager="true">
              <v-card class="mx-auto mb-0" flat tile>
                <v-card-text>
                  <v-row>
                    <v-col cols="12" md="4">
                      <v-text-field
                        v-model="curCli.codigo"
                        name="codigo"
                        label="Código"
                        dense
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="2">
                      <v-checkbox
                        v-model="curCli.is_cli"
                        name="is_cli"
                        label="Cliente"
                        class="mt-0"
                      ></v-checkbox>
                    </v-col>
                    <v-col cols="12" md="2">
                      <v-checkbox
                        v-model="curCli.is_pro"
                        name="is_pro"
                        label="Proveedor"
                        class="mt-0"
                      ></v-checkbox>
                    </v-col>
                    <v-col cols="12" md="2">
                      <v-checkbox
                        v-model="curCli.is_ban"
                        name="is_ban"
                        label="Banco"
                        class="mt-0"
                      ></v-checkbox>
                    </v-col>
                    <v-col cols="12" md="2">
                      <v-checkbox
                        v-model="curCli.is_soc"
                        name="is_soc"
                        label="Socio"
                        class="mt-0"
                      ></v-checkbox>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" md="4">
                      <v-checkbox
                        v-model="curCli.cred"
                        name="cred"
                        label="Cliente de Crédito"
                        class="mt-0"
                      >
                      </v-checkbox>
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-select
                        v-model="curCli.diascr"
                        :items="items_diascred"
                        name="diascr"
                        label="Días de Crédito"
                        dense
                      >
                      </v-select>
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-text-field
                        v-model="curCli.maxcr"
                        name="maxcr"
                        label="Máximo crédito"
                        dense
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" md="4">
                      <v-checkbox
                        v-model="curCli.ordencompra"
                        name="ordencompra"
                        label="Requerir Orden de Compra"
                        class="mt-0"
                      ></v-checkbox>
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-checkbox
                        v-model="curCli.exonerado"
                        name="exonerado"
                        label="Exonerado ITBMS"
                        class="mt-0"
                      ></v-checkbox>
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-text-field
                        v-model="curCli.retencion"
                        name="retencion"
                        label="Retención ITBMS"
                        dense
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" md="4">
                      <v-text-field
                        v-model="curCli.descauto"
                        name="descauto"
                        label="Descuento Automático"
                        dense
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-select
                        name="idgenerico"
                        label="ID Generico"
                        dense
                      ></v-select>
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-checkbox
                        v-model="curCli.is_active"
                        name="is_active"
                        label="Activo"
                        class="mt-0"
                      ></v-checkbox>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-tab-item>
            <v-tab-item key="3" :eager="true">
              <v-card class="mx-auto mb-0" flat tile>
                <v-card-text>
                  <v-row>
                    <v-col cols="12" md="4">
                      <v-menu
                        ref="bdmenu"
                        v-model="bdmenu"
                        :close-on-content-click="false"
                        transition="scale-transition"
                        offset-y
                        min-width="290px"
                      >
                        <template v-slot:activator="{ on, attrs }">
                          <v-text-field
                            v-model="curCli.birth_date"
                            name="birth_date"
                            label="Fecha Nacimiento"
                            prepend-icon="mdi-calendar"
                            readonly
                            dense
                            v-bind="attrs"
                            v-on="on"
                          ></v-text-field>
                        </template>
                        <v-date-picker
                          ref="bdpicker"
                          v-model="curCli.birth_date"
                          :max="new Date().toISOString().substr(0, 10)"
                          min="1920-01-01"
                          @change="bdSave"
                        ></v-date-picker>
                      </v-menu>
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-select
                        v-model="curCli.locale"
                        :items="items_locale"
                        item-text="name"
                        item-value="id"
                        name="locale"
                        label="Localización"
                        dense
                      ></v-select>
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-text-field
                        v-model="curCli.website"
                        name="website"
                        label="Web Site"
                        dense
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col>
                      <v-textarea
                        v-model="curCli.contacto"
                        name="contacto"
                        label="Contacto"
                        rows="2"
                      ></v-textarea>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-tab-item>
          </v-tabs-items>
        </v-form>
      </v-col>

      <v-col v-show="showsearch" class="shrink" cols="3">
        <v-expand-x-transition>
          <v-card
            v-show="showsearch"
            class="mx-auto pa-2 scroll borderleftonly"
            flat
            tile
            outlined
            :max-height="cardHeigt"
          >
            <DxList
              :data-source="dataSource"
              :search-enabled="true"
              :search-editor-options="{ placeholder: 'Buscar' }"
              class="mt-2"
              selection-mode="single"
              :selected-item-keys="[curCli.id]"
              :hover-state-enabled="true"
              :disabled="modo !== 'r'"
              @selection-changed="listSelectionChanged"
            >
              <template #item="{ data: item }">
                <div>
                  <b>{{ item.nombre }}</b>
                  <div>{{ currency(item.maxcr) }}</div>
                  <div>{{ item.codigo }}</div>
                  <v-divider></v-divider>
                </div>
              </template>
            </DxList>
          </v-card>
        </v-expand-x-transition>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import DxList from 'devextreme-vue/list'
import ArrayStore from 'devextreme/data/array_store'
import { clientes } from '~/assets/data.js'

// const formData = new FormData(this.$ref.curform)

const currencyFormatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
})

export default {
  components: {
    DxList,
  },

  data() {
    return {
      modo: 'r',
      curCli: {},
      dataSource: {
        store: new ArrayStore({
          data: clientes,
          key: 'id',
        }),
        searchExpr: ['id', 'nombre', 'codigo'],
      },
      sm: 'contains',
      cols_mainbody: 9,
      cols_serchtool: 3,
      showsearch: true,
      menu_items: [
        { title: 'Opc1' },
        { title: 'Opc2' },
        { title: 'Opc3' },
        { title: 'Opc4' },
      ],
      window_size: {
        width: 0,
        height: 0,
      },
      cardHeigt: 300,
      tab: null,
      items_persona: [
        { id: 'N', name: 'NATURAL' },
        { id: 'J', name: 'JURIDICA' },
      ],
      items_diascred: [15, 30, 45, 60, 90],
      items_locale: [
        { id: 'es_PA', name: 'Español PA' },
        { id: 'en_US', name: 'Inglés EEUU' },
      ],
      bdmenu: false,
    }
  },

  watch: {
    bdmenu(val) {
      val && setTimeout(() => (this.$refs.bdpicker.activePicker = 'YEAR'))
    },
  },

  created() {
    const cli = clientes.find(
      (cli) => cli.id === parseInt(this.$route.params.idcli)
    )
    this.curCli = cli
  },

  mounted() {
    window.addEventListener('resize', this.windowSize)
    this.windowSize()
  },

  destroyed() {
    window.removeEventListener('resize', this.windowSize)
  },

  methods: {
    showSearch() {
      this.cols_mainbody = this.cols_mainbody === 12 ? 9 : 12
      // this.cols_serchtool = this.cols_serchtool === 1 ? 2 : 1
      this.showsearch = !this.showsearch
    },
    currency(data) {
      return currencyFormatter.format(data)
    },
    listSelectionChanged(e) {
      const aux = e.addedItems[0]
      this.curCli = aux
    },
    windowSize() {
      this.window_size.height = window.innerHeight
      this.window_size.width = window.innerWidth
      this.cardHeigt = window.innerHeight * 0.6
    },
    bdSave(date) {
      this.$refs.bdmenu.save(date)
    },
  },

  head() {
    return {
      title: 'Cliente',
    }
  },
}
</script>

<style scoped>
.scroll {
  overflow-y: scroll;
}
.borderleftonly {
  border-top: solid white !important;
  border-bottom: solid white !important;
}
</style>
