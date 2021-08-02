<template>
  <div>
    <v-img
      :src="imgSrc"
      :lazy-src="lazySrc"
      contain
      max-width="175"
      @error="onImgError"
    >
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
export default {
  name: 'ImgForGrid',
  props: {
    imgFile: {
      type: String,
      required: true,
      default: 'noimg.jpg',
    },
    fullPath: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      lazySrc: this.$config.fotosURL + 'nophoto_sm.png',
      imgErr: false,
    }
  },
  computed: {
    imgSrc() {
      let imgsrc

      if (this.imgErr) {
        imgsrc = '/no_image.png'
      } else {
        imgsrc = this.imgFile
        if (!this.fullPath) {
          // imgsrc = this.$config.fotosURL + this.imgFile + this.$config.fotosExt
          imgsrc = this.$config.fotosURL + this.imgFile
        }
      }
      return imgsrc
    },
    imgID() {
      return this.imgFile.value
    },
  },
  mounted() {},
  methods: {
    onImgError() {
      this.imgErr = true
      this.$emit('no-image')
    },
  },
}
</script>

<style scoped></style>
