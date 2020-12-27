<template>
  <v-card class="mx-auto mt-10">
    <v-toolbar color="secondary" clipped-right dark fixed>
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

      <v-app-bar-nav-icon @click.stop="mini = !mini"></v-app-bar-nav-icon>
    </v-toolbar>
    <v-card class="mx-auto" flat tile>
      <v-navigation-drawer
        v-model="drawer"
        right
        absolute
        :mini-variant.sync="mini"
      >
        <v-list nav dense>
          <v-list-item-group
            v-model="group"
            active-class="deep-purple--text text--accent-4"
          >
            <v-list-item>
              <v-list-item-title>Foo</v-list-item-title>
            </v-list-item>

            <v-list-item>
              <v-list-item-title>Bar</v-list-item-title>
            </v-list-item>

            <v-list-item>
              <v-list-item-title>Fizz</v-list-item-title>
            </v-list-item>

            <v-list-item>
              <v-list-item-title>Buzz</v-list-item-title>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-navigation-drawer>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" md="6">
              <v-select
                v-model="selection"
                :items="items"
                multiple
                label="Select an option"
              >
              </v-select>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field label="Text Field"></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    drawer: true,
    mini: true,
    selection: [],
    items: ['Foo', 'Bar', 'Fizz', 'Buzz'],
    menu_items: [
      { title: 'Opc1' },
      { title: 'Opc2' },
      { title: 'Opc3' },
      { title: 'Opc4' },
    ],
    group: null,
  }),

  watch: {
    group() {
      this.mini = false
    },
  },
}
</script>

<style scoped></style>
