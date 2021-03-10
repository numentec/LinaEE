<template>
  <div>
    <v-img :src="imgPath" alt="NO IMAGE" contain width="200">
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
      type: Object,
      required: true,
      default: () => {},
    },
  },
  computed: {
    imgPath() {
      const basePath =
        'https://cloudadmin:WwEgk-tQowR-A2KLx-BNrCE-b7b4i@nube.vertigozl.net/remote.php/dav/files/cloudadmin/DemoFotos/'
      return basePath + this.imgFile.value + '.jpg/'
    },
  },
}
</script>

<style scoped></style>
