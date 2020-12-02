<template>
  <v-card class="mx-auto" max-width="300">
    <v-list flat max-height="300" class="overflow-y-auto">
      <v-list-item @click="selectAll">
        <template v-slot:default="{ active }">
          <v-list-item-action>
            <v-checkbox v-model="allCols" :input-value="active"></v-checkbox>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Todo</v-list-item-title>
          </v-list-item-content>
        </template>
      </v-list-item>

      <v-divider></v-divider>
      <v-list-item-group v-model="selected" multiple mandatory active-class="">
        <v-list-item
          v-for="header in colsHeaders"
          :key="header.text"
          :value="header"
          @click="hideCols(true)"
        >
          <template v-slot:default="{ active }">
            <v-list-item-action>
              <v-checkbox :input-value="active"></v-checkbox>
            </v-list-item-action>

            <v-list-item-content>
              <v-list-item-title>{{ header.text }}</v-list-item-title>
            </v-list-item-content>
          </template>
        </v-list-item>
      </v-list-item-group>
    </v-list>
    <v-divider></v-divider>
    <v-card-actions>
      <v-btn block color="accent lighten-4" @click="hideCols()">
        Aplicar
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'SelCols',
  props: {
    colsHeaders: {
      type: Array,
      required: false,
      default() {
        return []
      },
    },
  },
  data() {
    return {
      selected: [],
      allCols: true,
    }
  },
  mounted() {
    this.selectAll()
  },
  methods: {
    hideCols(shown = false) {
      setTimeout(() =>
        this.$emit('hide-cols', { menu: shown, colssel: this.selected })
      )
    },
    selectAll() {
      if (this.allCols) {
        this.selected = this.colsHeaders
      } else {
        this.selected = []
      }
    },
  },
}
</script>
