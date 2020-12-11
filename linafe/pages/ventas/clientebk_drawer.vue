<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card class="mx-auto mt-10">
          <v-toolbar color="secondary" dark clipped-right fixed>
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
              {{
                selection.length ? `${selection.length} selected` : 'Cliente'
              }}
            </v-toolbar-title>

            <v-spacer></v-spacer>

            <v-app-bar-nav-icon
              @click.stop="drawer = !drawer"
            ></v-app-bar-nav-icon>
          </v-toolbar>
          <v-card class="mx-auto">
            <v-navigation-drawer v-model="drawer" clipped absolute right fixed>
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
              <v-select
                v-model="selection"
                :items="items"
                multiple
                label="Select an option"
              ></v-select>
            </v-card-text>
          </v-card>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
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

  watch: {
    group() {
      this.drawer = false
    },
  },
}
</script>

<style scoped></style>
