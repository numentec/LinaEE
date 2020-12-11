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
    <v-container>
      <v-row>
        <v-col class="shrink" :cols="cols_mainbody">
          <v-card class="mx-auto" flat tile style="max-height: 300px">
            <p>
              {{ cols_mainbody }}
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Cum ab
              similique explicabo et neque doloremque eveniet harum? Atque error
              alias exercitationem ratione id sequi blanditiis, animi iste enim
              voluptatem aliquid? Lorem ipsum dolor sit amet consectetur
              adipisicing elit. Cum ab similique explicabo et neque doloremque
              eveniet harum? Atque error alias exercitationem ratione id sequi
              blanditiis, animi iste enim voluptatem aliquid? Lorem ipsum dolor
              sit amet consectetur adipisicing elit. Cum ab similique explicabo
              et neque doloremque eveniet harum? Atque error alias
              exercitationem ratione id sequi blanditiis, animi iste enim
              voluptatem aliquid?
              {{ cardHeigt }}
            </p>
            <div><v-divider class="mx-2" vertical></v-divider></div>
          </v-card>
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
              <v-text-field
                v-model="search"
                prepend-icon="mdi-magnify"
                clearable
                placeholder="Buscar"
                @click:clear="setData"
              ></v-text-field>
              <v-list tow-line>
                <v-list-item-group
                  v-model="selectedItem"
                  active-class="accent lighten-5"
                >
                  <template v-for="(product, index) in filteredProducts">
                    <v-list-item :key="product.Name">
                      <v-list-item-content>
                        <v-list-item-title
                          v-text="product.Name"
                        ></v-list-item-title>
                        <v-list-item-subtitle
                          v-text="product.Price"
                        ></v-list-item-subtitle>
                        <v-list-item-subtitle
                          v-text="product.Category"
                        ></v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                    <v-divider :key="index"></v-divider>
                  </template>
                </v-list-item-group>
              </v-list>
            </v-card>
          </v-expand-x-transition>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
import { products } from '~/assets/data.js'

const currencyFormatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
})

export default {
  data: () => ({
    selectedItem: 0,
    search: '',
    searchItem: [],
    curCli: [],
    products,
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
  }),

  computed: {
    filteredProducts() {
      return this.searchItem.filter((item) => {
        return (
          item.Name.toLowerCase().match(this.search) ||
          item.Category.toLowerCase().match(this.search)
        )
      })
    },
  },

  mounted() {
    window.addEventListener('resize', this.windowSize)
    this.windowSize()
    this.setData()
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
      this.curCli = e.addedItems[0]
      alert(this.curCli.Nombre)
    },
    windowSize() {
      this.window_size.height = window.innerHeight
      this.window_size.width = window.innerWidth
      this.cardHeigt = window.innerHeight * 0.6
    },
    setData() {
      setTimeout(() => (this.searchItem = this.products))
      // alert('Hi')
    },
  },
}
</script>

<style scoped>
.scroll {
  overflow-y: scroll;
}
</style>
