<template>
  <div>
    <DxPopup
      :max-width="800"
      :max-height="600"
      :drag-enabled="false"
      :close-on-outside-click="true"
      :visible="showSlideshow"
      @hidden="$emit('hideSlideshow')"
    >
      <template>
        <div>
          <DxGallery
            :data-source="dS"
            :show-nav-buttons="true"
            :show-indicator="true"
            :max-height="400"
            :loop="true"
            :selected-index="curIndex"
            width="100%"
            @item-click="selx"
          >
            <template #item="{ data }">
              <div>
                <img :src="imgSrc(data.SKU)" />
              </div>
            </template>
          </DxGallery>
        </div>
      </template>
      <DxToolbarItem
        :options="buttonOptions"
        widget="dxButton"
        location="before"
      />
      <DxDrawer
        opened-state-mode="overlap"
        position="left"
        reveal-mode="slide"
        :opened="openDetails"
        :height="300"
        :close-on-outside-click="true"
        template="listMenu"
      >
        <template #listMenu>
          <div>
            <h1>HELLO!!!</h1>
          </div>
        </template>
      </DxDrawer>
    </DxPopup>
  </div>
</template>

<script>
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup'
import DxGallery from 'devextreme-vue/gallery'
import DxDrawer from 'devextreme-vue/drawer'

export default {
  name: 'Slideshow',
  components: {
    DxPopup,
    DxToolbarItem,
    DxGallery,
    DxDrawer,
  },
  props: {
    showSlideshow: {
      type: Boolean,
      default: false,
    },
    curKey: {
      type: String,
      default: '',
    },
    curIndex: {
      type: Number,
      default: 0,
    },
    dataSource: {
      type: Object,
      default: () => {},
    },
  },

  data() {
    return {
      openDetails: false,
      buttonOptions: {
        icon: 'menu',
        onClick: () => {
          this.openDetails = !this.openDetails
        },
      },
    }
  },
  computed: {
    dS() {
      let ds = {}
      if (this.dataSource) {
        ds = this.dataSource
      }
      return ds
    },
  },
  methods: {
    imgSrc(key) {
      const imgsrc = this.$config.fotosURL + key + this.$config.fotosExt
      return imgsrc
    },
    selx(e) {
      // console.log('ALL e', e)
    },
  },
}
</script>

<style scoped>
.img {
  object-fit: contain;
}
</style>
