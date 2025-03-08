/* eslint-disable no-console */
<template>
  <client-only>
    <v-dialog
      :value="showSlideshow"
      persistent
      max-width="850px"
      min-width="200px"
      @keydown.esc="$emit('hideSlideshow')"
    >
      <v-card flat tile class="mx-auto">
        <v-app-bar color="white" flat>
          <v-spacer />
          <v-btn icon @click="$emit('hideSlideshow')">
            <v-icon>mdi-window-close</v-icon>
          </v-btn>
        </v-app-bar>
        <v-container>
          <v-row justify="center">
            <v-col align="center" justify="center" class="shrink" cols="12">
              <v-card flat tile class="mx-auto">
                <v-container>
                  <v-carousel v-model="curItem" hide-delimiters>
                    <v-carousel-item v-for="(item, i) in dS" :key="i">
                      <v-container>
                        <v-img
                          :src="imgSrc(item)"
                          contain
                          max-width="700"
                          max-height="500"
                        >
                          <template v-slot:placeholder>
                            <v-row
                              class="fill-height ma-0"
                              align="center"
                              justify="center"
                            >
                              <v-progress-circular
                                indeterminate
                                color="grey lighten-5"
                              >
                              </v-progress-circular>
                            </v-row>
                          </template>
                        </v-img>
                      </v-container>
                    </v-carousel-item>
                  </v-carousel>
                </v-container>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-dialog>
  </client-only>
</template>

<script>
export default {
  name: 'Slideshow',
  props: {
    showSlideshow: {
      type: Boolean,
      default: false,
    },
    dataSource: {
      type: Array,
      default: () => [],
    },
  },

  data() {
    return {
      curItem: 0,
    }
  },
  computed: {
    // Datasource array form
    dS() {
      let ds = []
      if (this.dataSource) {
        ds = this.dataSource
      }
      return ds
    },
  },

  mounted() {},

  methods: {
    imgSrc(foto) {
      let imgsrc = '/no_image.png'

      if (foto) {
        imgsrc = foto
      }

      return imgsrc
    },
  },
}
</script>

<style scoped></style>
