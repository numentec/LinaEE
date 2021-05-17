<template>
  <div>
    <v-card class="mx-auto mt-10">
      <v-toolbar color="secondary" dense dark fixed>
        <v-menu offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on">
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>

          <v-list nav dense>
            <v-list-item
              v-for="(item, i) in menu_items"
              :key="i"
              :disabled="item.disabled"
              link
              @click="item.method"
            >
              <v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-menu>

        <v-toolbar-title>{{ toolbar_title }}</v-toolbar-title>

        <v-spacer></v-spacer>
        <div v-show="modo !== 'r'" class="mr-4">
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon v-bind="attrs" v-on="on" @click="saveProfile">
                <v-icon>mdi-content-save-outline</v-icon>
              </v-btn>
            </template>
            <span>Guardar</span>
          </v-tooltip>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon v-bind="attrs" v-on="on" @click="cancelEdit">
                <v-icon>mdi-undo</v-icon>
              </v-btn>
            </template>
            <span>Cancelar</span>
          </v-tooltip>
        </div>

        <v-app-bar-nav-icon @click.stop="showSearch">
          <v-icon v-if="showsearch">mdi-arrow-collapse-horizontal</v-icon>
          <v-icon v-else>mdi-magnify</v-icon>
        </v-app-bar-nav-icon>
        <template v-slot:extension>
          <v-tabs v-model="tab" grow dense dark>
            <v-tab key="1">General</v-tab>
            <v-tab key="2">Configuración</v-tab>
          </v-tabs>
        </template>
      </v-toolbar>
      <v-row>
        <v-col class="shrink" :cols="cols_mainbody">
          <v-form
            ref="curform"
            v-model="valid"
            lazy-validation
            @submit.prevent="submit"
          >
            <v-tabs-items v-model="tab">
              <v-tab-item
                key="1"
                :class="showsearch ? 'pl-4' : 'px-4'"
                :eager="true"
              >
                <v-card class="mx-auto mb-0" flat tile>
                  <v-row>
                    <v-col align="center" justify="center" cols="12" md="4">
                      <div id="dropzone-frame">
                        <v-hover v-slot="{ hover }">
                          <v-card
                            :elevation="
                              (hover || isDropZoneActive) && modo != 'r'
                                ? 12
                                : 0
                            "
                            :class="{ 'on-hover': hover }"
                            max-width="200"
                          >
                            <v-img
                              :src="imageSource"
                              alt="NO PHOTO"
                              contain
                              max-height="150"
                            >
                              <v-card-text class="title white--text">
                                <v-row class="flex-column" justify="center">
                                  <v-col class="align-self-center">
                                    <v-btn
                                      v-show="
                                        (hover || isDropZoneActive) &&
                                        modo != 'r'
                                      "
                                      fab
                                      dark
                                      large
                                      color="rgba(50, 50, 50, 0.5)"
                                    >
                                      <v-icon
                                        v-show="isDropZoneActive"
                                        dark
                                        x-large
                                      >
                                        mdi-cloud-upload
                                      </v-icon>
                                      <v-icon
                                        v-show="!isDropZoneActive"
                                        dark
                                        x-large
                                      >
                                        mdi-image-edit-outline
                                      </v-icon>
                                    </v-btn>
                                    <DxProgressBar
                                      id="upload-progress"
                                      :min="0"
                                      :max="100"
                                      width="30%"
                                      :show-status="false"
                                      :visible="progressVisible"
                                      :value="progressValue"
                                    />
                                  </v-col>
                                </v-row>
                              </v-card-text>
                            </v-img>
                          </v-card>
                        </v-hover>
                      </div>
                    </v-col>
                    <v-col cols="12" md="8">
                      <v-row>
                        <v-col cols="6">
                          <v-text-field
                            v-model="curUser.first_name"
                            :rules="[rules.required]"
                            name="nombre"
                            :readonly="modo == 'r'"
                            label="Nombres"
                            dense
                          ></v-text-field>
                        </v-col>
                        <v-col cols="6">
                          <v-text-field
                            v-model="curUser.last_name"
                            :rules="[rules.required]"
                            name="nombre"
                            :readonly="modo == 'r'"
                            label="Apellidos"
                            dense
                          ></v-text-field>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="6">
                          <v-text-field
                            v-model="curUser.dni"
                            name="dv"
                            :readonly="modo == 'r'"
                            label="DNI"
                            dense
                          ></v-text-field>
                        </v-col>
                        <v-col cols="6">
                          <v-select
                            v-model="curUser.localization"
                            :items="items_locale"
                            item-text="name"
                            item-value="id"
                            name="localization"
                            :readonly="modo == 'r'"
                            label="Idioma"
                            dense
                            class="mt-0"
                          ></v-select>
                        </v-col>
                      </v-row>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" md="4">
                      <v-text-field
                        v-model="curUser.email"
                        :rules="[rules.email]"
                        name="email"
                        :readonly="modo == 'r'"
                        label="E-mail"
                        dense
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-text-field
                        v-model="curUser.tel1"
                        name="tel1"
                        :readonly="modo == 'r'"
                        label="WhatsApp"
                        dense
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-text-field
                        v-model="curUser.tel2"
                        name="tel2"
                        :readonly="modo == 'r'"
                        label="Teléfono"
                        dense
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" md="4">
                      <v-text-field
                        v-model="curUser.nombre_corto"
                        name="nombre_corto"
                        :readonly="modo == 'r'"
                        label="Nombre Corto"
                        dense
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-menu
                        ref="bdmenu"
                        v-model="bdmenu"
                        :close-on-content-click="false"
                        transition="scale-transition"
                        offset-y
                        min-width="290px"
                      >
                        <template v-slot:activator="{ on, attrs }">
                          <v-text-field
                            v-model="curUser.birth_date"
                            name="birth_date"
                            label="Fecha de Nacimiento"
                            prepend-icon="mdi-calendar"
                            readonly
                            dense
                            v-bind="attrs"
                            v-on="on"
                          ></v-text-field>
                        </template>
                        <v-date-picker
                          ref="bdpicker"
                          v-model="curUser.birth_date"
                          :readonly="modo == 'r'"
                          :max="new Date().toISOString().substr(0, 10)"
                          min="1920-01-01"
                          @change="bdSave"
                        ></v-date-picker>
                      </v-menu>
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-textarea
                        v-model="curUser.direccion"
                        name="direccion"
                        :readonly="modo == 'r'"
                        label="Dirección"
                        rows="2"
                        dense
                      ></v-textarea>
                    </v-col>
                  </v-row>
                </v-card>
              </v-tab-item>
              <v-tab-item
                key="2"
                :class="showsearch ? 'pl-4' : 'px-4'"
                :eager="true"
              >
                <v-card class="mx-auto mb-0" flat tile>
                  <v-row>
                    <v-col cols="12" md="8">
                      <v-select
                        v-model="curUser.groups"
                        :items="userGroups"
                        item-text="name"
                        item-value="id"
                        prepend-icon="mdi-account-multiple-check-outline"
                        multiple
                        label="Grupos"
                        chips
                        deletable-chips
                      >
                      </v-select>
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-checkbox
                        v-model="curUser.is_active"
                        name="is_active"
                        :readonly="modo == 'r'"
                        label="Activo"
                        class="mt-0"
                      ></v-checkbox>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" md="8">
                      <v-textarea
                        v-model="curUser.bio"
                        name="bio"
                        :readonly="modo == 'r'"
                        label="Biografía"
                        dense
                        outlined
                      ></v-textarea>
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-text-field
                        v-model="curUser.tel3"
                        name="tel3"
                        :readonly="modo == 'r'"
                        label="Teléfono (2)"
                        dense
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" md="4">
                      <v-text-field
                        v-model="curUser.date_joined"
                        name="registro"
                        :readonly="true"
                        label="Registro"
                        dense
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-text-field
                        v-model="curUser.last_login"
                        name="last_login"
                        :readonly="true"
                        label="Último acceso"
                        dense
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-card>
              </v-tab-item>
            </v-tabs-items>
          </v-form>
        </v-col>

        <v-col v-show="showsearch" class="shrink" cols="3">
          <v-expand-x-transition>
            <v-card
              v-show="showsearch"
              class="mx-auto pa-2 borderleftonly"
              flat
              tile
              outlined
              :height="cardHeigt"
            >
              <DxList
                :ref="searchList"
                :data-source="dataSource"
                :search-enabled="true"
                :search-editor-options="{ placeholder: 'Buscar' }"
                class="mt-2"
                selection-mode="single"
                :selected-item-keys="listSelectedKeys"
                :hover-state-enabled="true"
                :disabled="modo !== 'r'"
                @selection-changed="listSelectionChanged"
              >
                <template #item="{ data: item }">
                  <div>
                    <b>{{ item.fullname }}</b>
                    <div>{{ item.username }}</div>
                    <div>{{ item.id }}</div>
                    <v-divider></v-divider>
                  </div>
                </template>
              </DxList>
            </v-card>
          </v-expand-x-transition>
        </v-col>
      </v-row>
    </v-card>
    <DxFileUploader
      id="file-uploader"
      :disabled="modo == 'r'"
      dialog-trigger="#dropzone-frame"
      drop-zone="#dropzone-frame"
      :multiple="false"
      :allowed-file-extensions="allowedFileExtensions"
      upload-mode="instantly"
      upload-url=""
      :visible="false"
      @drop-zone-enter="onDropZoneEnter"
      @drop-zone-leave="onDropZoneLeave"
      @uploaded="onUploaded"
      @progress="onProgress"
      @upload-started="onUploadStarted"
    />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import DxList from 'devextreme-vue/list'
import DataSource from 'devextreme/data/data_source'
import { DxFileUploader } from 'devextreme-vue/file-uploader'
import { DxProgressBar } from 'devextreme-vue/progress-bar'

const searchList = 'search-list'
// const formData = new FormData(this.$ref.curform)

const currencyFormatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
})

export default {
  name: 'Perfil',

  validate({ route }) {
    return /^\d+$/.test(route.params.iduser)
  },

  components: {
    DxList,
    DxFileUploader,
    DxProgressBar,
  },

  async fetch() {
    // Lista de grupos
    try {
      this.userGroups = await this.$axios
        .get('groups/')
        .then((response) => response.data)
    } catch (err) {
      if (err.response) {
        this.error({
          statusCode: err.response.status,
          message: err.response.data.detail,
        })
      } else {
        this.error({
          statusCode: 503,
          message: 'No se pudo cargar la lista de grupos. Intente luego',
        })
      }
    }
  },

  data() {
    return {
      modo: 'r',
      searchList,
      curUser: {},
      dataSource: null,
      listSelectedKeys: [],
      userGroups: [],
      toolbar_title: 'Perfil - Consultar',
      sm: 'contains',
      cols_mainbody: 9,
      cols_serchtool: 3,
      showsearch: true,
      window_size: {
        width: 0,
        height: 0,
      },
      cardHeigt: 300,
      tab: null,
      items_locale: [
        { id: 'es_PA', name: 'Español PA' },
        { id: 'en_US', name: 'Inglés EEUU' },
      ],
      bdmenu: false,
      imageSource: '',
      isDropZoneActive: false,
      progressVisible: false,
      progressValue: 0,
      allowedFileExtensions: ['.jpg', '.jpeg', '.gif', '.png'],
      valid: true,
      rules: {
        required: (v) => {
          if (this.modo === 'r') {
            return true
          } else {
            return !!v.trim() || 'Requerido'
          }
        },
        email: (v) => {
          if (this.modo === 'r') {
            return true
          } else {
            return /.+@.+\..+/.test(v) || 'E-mail no válido'
          }
        },
        onlyplusfloat: (v) =>
          /^[+]?[0-9]*.?[0-9]+$/.test(v) || 'Cantidad no válido',
      },
    }
  },

  computed: {
    ...mapGetters('sistema', ['getUsers']),
    menu_items() {
      return [
        {
          title: 'Editar',
          icon: 'mdi-account-edit-outline',
          disabled: this.modo !== 'r',
          method: () => this.editProfile(),
        },
        {
          title: 'Guardar',
          icon: 'mdi-content-save-outline',
          disabled: this.modo === 'r',
          method: () => this.saveProfile(),
        },
        {
          title: 'Cancelar',
          icon: 'mdi-undo',
          disabled: this.modo === 'r',
          method: () => this.cancelEdit(),
        },
      ]
    },
    sList() {
      return this.$refs[searchList].instance
    },
  },

  watch: {
    bdmenu(val) {
      val && setTimeout(() => (this.$refs.bdpicker.activePicker = 'YEAR'))
    },
  },

  created() {
    this.dataSource = new DataSource({
      store: {
        type: 'array',
        key: 'id',
        data: this.getUsers,
      },
      searchExpr: ['id', 'fullname', 'username'],
    })
  },

  mounted() {
    window.addEventListener('resize', this.windowSize)
    this.windowSize()
    const usr = this.getUsers.find(
      (usr) => usr.id === parseInt(this.$route.params.iduser)
    )
    this.curUser = JSON.parse(JSON.stringify(usr))
    this.modo = 'r'
    this.listSelectedKeys = [usr.id]
  },

  destroyed() {
    window.removeEventListener('resize', this.windowSize)
  },

  methods: {
    showSearch() {
      this.cols_mainbody = this.cols_mainbody === 12 ? 9 : 12
      // this.cols_serchtool = this.cols_serchtool === 1 ? 2 : 1
      this.showsearch = !this.showsearch
    },
    currency(data) {
      return currencyFormatter.format(data)
    },
    listSelectionChanged(e) {
      const usr = e.addedItems[0]
      this.curUser = JSON.parse(JSON.stringify(usr))
      this.imageSource = this.curUser.foto
    },
    windowSize() {
      this.window_size.height = window.innerHeight
      this.window_size.width = window.innerWidth
      this.cardHeigt = window.innerHeight * 0.6
    },
    // Upload image methods
    onDropZoneEnter(e) {
      if (e.dropZoneElement.id === 'dropzone-frame') {
        this.isDropZoneActive = true
      }
    },
    onDropZoneLeave(e) {
      if (e.dropZoneElement.id === 'dropzone-frame') {
        this.isDropZoneActive = false
      }
    },
    onUploaded(e) {
      const file = e.file
      const fileReader = new FileReader()
      fileReader.onload = () => {
        this.isDropZoneActive = false
        this.imageSource = fileReader.result
      }
      fileReader.readAsDataURL(file)
      this.textVisible = false
      this.progressVisible = false
      this.progressValue = 0
    },
    onProgress(e) {
      this.progressValue = (e.bytesLoaded / e.bytesTotal) * 100
    },
    onUploadStarted() {
      this.imageSource = ''
      this.progressVisible = true
    },
    // Ends upload image methods
    bdSave(date) {
      this.$refs.bdmenu.save(date)
    },
    reset() {
      this.$refs.curform.reset()
    },
    resetValidation() {
      this.$refs.curform.resetValidation()
    },
    editProfile() {
      this.modo = 'e'
    },
    saveProfile() {
      this.modo = 'r'
    },
    cancelEdit() {
      const selitems = this.sList.option('selectedItems')
      setTimeout(() => (this.listSelectedKeys = [this.getUsers[0].id]), 100)
      setTimeout(() => (this.listSelectedKeys = [selitems[0].id]), 150)
      this.modo = 'r'
    },
  },

  head() {
    return {
      title: 'Perfil',
    }
  },
}
</script>

<style scoped>
.scroll {
  overflow-y: scroll;
}
.borderleftonly {
  border-top: solid white !important;
  border-bottom: solid white !important;
}
</style>
