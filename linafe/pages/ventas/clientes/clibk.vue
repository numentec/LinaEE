<template>
  <v-card class="mx-auto mt-10">
    <v-toolbar color="secondary" dark fixed>
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
    </v-toolbar>
    <v-row>
      <v-col class="shrink" :cols="cols_mainbody">
        <v-form>
          <v-container class="test3 py-0">
            <v-row>
              <v-col cols="12" md="4">
                <div>ID: 507</div>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field label="Código" class="mt-2"></v-text-field>
              </v-col>
              <v-col cols="12" md="4" class="mt-2">
                <v-checkbox label="Activo"></v-checkbox>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="4">
                <v-text-field label="Nombre"></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field label="RUC"></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field label="DV"></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-tabs v-model="tab" grow background-color="formtabs">
                <v-tab key="1">Pag. 1</v-tab>
                <v-tab key="2">Pag. 2</v-tab>
                <v-tab key="3">Pag. 3</v-tab>
              </v-tabs>
              <v-tabs-items v-model="tab">
                <v-tab-item key="1" class="test2 pa-2" :eager="true">
                  <v-row>
                    <v-col cols="12" md="4">
                      <v-text-field label="Tel1"></v-text-field>
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-text-field label="Tel2"></v-text-field>
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-text-field label="Tel3"></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col>
                      <p>
                        Lorem ipsum dolor sit amet consectetur adipisicing elit.
                        Cum ab similique explicabo et neque doloremque eveniet
                        harum?
                      </p>
                    </v-col>
                    <v-col>
                      <p>
                        Lorem ipsum dolor sit amet consectetur adipisicing elit.
                        Cum ab similique explicabo et neque doloremque eveniet
                        harum?
                      </p>
                    </v-col>
                    <v-col>
                      <p>
                        Lorem ipsum dolor sit amet consectetur adipisicing elit.
                        Cum ab similique explicabo et neque doloremque eveniet
                        harum?
                      </p>
                    </v-col>
                  </v-row>
                </v-tab-item>
                <v-tab-item key="2" :eager="true">
                  <v-card class="mb-0" color="yellow" flat tile>
                    <v-card-text>
                      <p>
                        {{ cols_mainbody }}
                        Lorem ipsum dolor sit amet consectetur adipisicing elit.
                        Cum ab similique explicabo et neque doloremque eveniet
                        harum? Atque error alias exercitationem ratione id sequi
                        blanditiis, animi iste enim voluptatem aliquid?
                      </p>
                      <br />
                      <div v-if="curCli">
                        <p>*********** {{ curCli.Name }} *********</p>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-tab-item>
                <v-tab-item key="3" :eager="true">
                  <v-card class="mb-0" color="blue" flat tile>
                    <v-card-text>
                      <p>
                        {{ cols_mainbody }}
                        Lorem ipsum dolor sit amet consectetur adipisicing elit.
                        Cum ab similique explicabo et neque doloremque eveniet
                        harum? Atque error alias exercitationem ratione id sequi
                        blanditiis, animi iste enim voluptatem aliquid?
                      </p>
                      <br />
                      <div v-if="curCli">
                        <p>*********** {{ curCli.Price }} *********</p>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-tab-item>
              </v-tabs-items>
            </v-row>
          </v-container>
        </v-form>
      </v-col>

      <v-col v-show="showsearch" class="shrink" cols="3">
        <v-expand-x-transition>
          <v-card
            v-show="showsearch"
            class="mx-auto pa-2 scroll"
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
              :selected-item-keys="[curCli.ID]"
              @selection-changed="listSelectionChanged"
            >
              <template #item="{ data: item }">
                <div>
                  <b>{{ item.Name }}</b>
                  <div>{{ currency(item.Price) }}</div>
                  <div>{{ item.Category }}</div>
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
import { products } from '~/assets/data.js'

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
      curCli: {},
      dataSource: {
        store: new ArrayStore({
          data: products,
          key: 'ID',
        }),
        searchExpr: ['ID', 'Name', 'Category'],
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
    }
  },

  created() {
    const prod = products.find(
      (prod) => prod.ID === parseInt(this.$route.params.idcli)
    )
    this.curCli = prod
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
.test1 {
  background-color: coral;
}
.test2 {
  background-color: yellow;
}
.test3 {
  background-color: blue;
}
</style>
