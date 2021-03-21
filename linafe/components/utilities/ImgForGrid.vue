<template>
  <div>
    <v-img :src="imgSrc" :lazy-src="lazySrc" contain max-width="200">
      <template v-slot:placeholder>
        <v-row class="fill-height ma-0" align="center" justify="center">
          <v-progress-circular
            indeterminate
            color="grey lighten-5"
          ></v-progress-circular>
        </v-row>
      </template>
    </v-img>
  </div>
</template>

<script>
import LinaConfig from '~/linaconfig.js'

export default {
  name: 'ImgForGrid',
  props: {
    imgFile: {
      type: Object,
      required: true,
      default: () => {},
    },
  },
  data() {
    return {
      // lazySrc: process.env.SERVER_URL_CLIENT + '/media/images/nophoto_sm.png',
      lazySrc: LinaConfig.PUBLIC_URL + 'media/images/nophoto_sm.png',
    }
  },
  computed: {
    imgSrc() {
      // return process.env.IMGBASEPATH + this.imgFile.value + process.env.IMGEXT
      return LinaConfig.IMGBASEPATH + this.imgFile.value + LinaConfig.IMGEXT
    },
  },
}
</script>

<style scoped></style>
