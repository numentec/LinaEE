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
        <v-app-bar
          :color="showTitle ? 'accent darken-3' : 'white'"
          :dark="showTitle"
          :flat="!showTitle"
          :elevated="showTitle"
        >
          <v-app-bar-nav-icon @click.stop="showDetails">
            <v-icon v-show="showdetails">
              mdi-arrow-collapse-horizontal
            </v-icon>
            <v-icon v-show="!showdetails">mdi-arrow-split-vertical</v-icon>
          </v-app-bar-nav-icon>
          <v-toolbar-title v-show="showTitle">Fotos Slideshow</v-toolbar-title>
          <v-spacer />
          <v-btn icon @click="$emit('hideSlideshow')">
            <v-icon>mdi-window-close</v-icon>
          </v-btn>
        </v-app-bar>
        <v-container>
          <v-row justify="center">
            <v-col
              align="center"
              justify="center"
              class="shrink"
              :cols="cols_mainbody"
            >
              <v-card flat tile class="mx-auto">
                <v-container>
                  <v-carousel v-model="curItem" hide-delimiters>
                    <v-carousel-item v-for="(item, i) in dS" :key="i">
                      <v-container>
                        <v-img
                          :src="imgSrc(item.FOTO)"
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
            <v-col v-show="showdetails" class="shrink" :cols="cols_serchtool">
              <v-expand-x-transition>
                <v-card
                  v-show="showdetails"
                  class="mx-auto pa-2 borderleftonly"
                  flat
                  tile
                  outlined
                >
                  <v-virtual-scroll
                    :bench="bench"
                    :items="itemDetails"
                    :item-height="50"
                    max-height="500"
                    max-width="300"
                  >
                    <template v-slot:default="{ item }">
                      <v-list-item>
                        <v-list-item-content>
                          <v-list-item-title>{{ item }}</v-list-item-title>
                        </v-list-item-content>
                      </v-list-item>
                    </template>
                  </v-virtual-scroll>
                </v-card>
              </v-expand-x-transition>
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
    curKey: {
      type: Number,
      default: 0,
    },
    dataSource: {
      type: Array,
      default: () => [],
    },
    noImgList: {
      type: Array,
      default: () => [],
    },
    showTitle: {
      type: Boolean,
      default: true,
    },
  },

  data() {
    return {
      showdetails: false,
      cols_mainbody: 12,
      cols_serchtool: 5,
      curItem: 0,
      bench: 10,
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
    // Return array from item-object's properties
    itemDetails() {
      let newArr = []

      const curItemObj = this.dS[this.curItem]
      if (curItemObj) {
        const objectArray = Object.entries(curItemObj)
        newArr = Array.from(objectArray, (obj) => `${obj[0]}: ${obj[1]}`)
      }

      return newArr
    },
  },
  watch: {
    // curKey(newVal) {
    //   // if (this.curKey !== 'non') {
    //   const ci = this.dS.findIndex((obj) => obj.ID === newVal)
    //   this.curItem = ci
    //   //   this.curKey = 'non'
    //   // }
    // },
    showSlideshow(newVal) {
      if (newVal) {
        const ci = this.dS.findIndex((obj) => obj.ID === this.curKey)
        this.curItem = ci
      }
    },
  },
  mounted() {},
  // activated() {
  //   const valx = this.$store.state.linabi.common.slidecurkey
  //   console.log('VUEX STORE VALUE', valx)
  // },
  // activated() {
  //   console.log('activate')
  //   const ci = this.dS.findIndex((obj) => obj.SKU === this.curKey)
  //   this.curItem = ci
  //   console.log('CURITEM VALUE', this.curItem)
  //   console.log('CURKEY VALUE', this.curKey)
  // },
  // deactivated() {
  //   console.log('deactivated')
  // },
  methods: {
    imgSrc(foto) {
      let imgsrc = '/no_image.png'

      if (!this.noImgList.includes(foto)) {
        imgsrc = this.$config.fotosURL + foto // + this.$config.fotosExt
      }

      return imgsrc
    },
    showDetails() {
      this.showdetails = !this.showdetails
      this.cols_mainbody = this.cols_mainbody === 12 ? 7 : 12
    },
  },
}
</script>

<style scoped>
.borderleftonly {
  border-top: solid white !important;
  border-bottom: solid white !important;
  border-right: solid white !important;
}
</style>
