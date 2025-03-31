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
        <v-btn
          fab
          right
          small
          absolute
          class="mt-4"
          @click="$emit('hideSlideshow')"
        >
          <v-icon>mdi-window-close</v-icon>
        </v-btn>
        <v-container>
          <v-row justify="center">
            <v-col align="center" justify="center">
              <v-carousel
                v-show="dS.length !== 0"
                v-model="curItem"
                :hide-delimiters="!isMobile"
                :show-arrows="!isMobile"
              >
                <v-carousel-item v-for="(item, i) in dS" :key="i">
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
                </v-carousel-item>
              </v-carousel>
              <v-alert
                v-show="dS.length === 0"
                dense
                border="left"
                type="warning"
              >
                <strong>No aditional image found!</strong>
              </v-alert>
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
    isMobile() {
      return this.$vuetify.breakpoint.smAndDown
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
