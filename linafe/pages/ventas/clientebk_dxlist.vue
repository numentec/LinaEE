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

      <v-toolbar-title>
        {{ selection.length ? `${selection.length} selected` : 'Cliente' }}
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-app-bar-nav-icon @click.stop="showSearch">
        <v-icon v-if="showsearch">mdi-arrow-collapse-horizontal</v-icon>
        <v-icon v-else>mdi-magnify</v-icon>
      </v-app-bar-nav-icon>
    </v-toolbar>
    <v-container>
      <v-row>
        <v-col class="shrink" :cols="cols_mainbody">
          <v-card class="mx-auto" flat tile transition="slide-x-transition">
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
              {{ showsearch }}
            </p>
            <div><v-divider class="mx-2" vertical></v-divider></div>
          </v-card>
        </v-col>

        <v-col v-show="showsearch" class="shrink" cols="3">
          <v-expand-x-transition>
            <v-card v-show="showsearch" class="mx-auto pa-2" flat tile outlined>
              <DxList
                :data-source="products"
                :height="350"
                :search-enabled="true"
                :search-mode="sm"
                :search-expr="['Name', 'Category']"
                class="mt-2"
                :selected-item-keys="[curCli.Nombre]"
                @selection-changed="listSelectionChanged"
              >
                <template #item="{ data }">
                  <div>
                    <b>{{ data.Name }}</b>
                    <div>{{ currency(data.Price) }}</div>
                    <div>{{ data.Category }}</div>
                    <v-divider></v-divider>
                  </div>
                </template>
              </DxList>
            </v-card>
          </v-expand-x-transition>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
import DxList from 'devextreme-vue/list'
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
  data: () => ({
    curCli: [],
    products,
    sm: 'contains',
    cols_mainbody: 9,
    cols_serchtool: 3,
    showsearch: true,
    drawer: false,
    group: null,
    selection: [],
    items: ['Foo', 'Bar', 'Fizz', 'Buzz'],
    menu_items: [
      { title: 'Opc1' },
      { title: 'Opc2' },
      { title: 'Opc3' },
      { title: 'Opc4' },
    ],
  }),

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
  },
}
</script>

<style scoped></style>
