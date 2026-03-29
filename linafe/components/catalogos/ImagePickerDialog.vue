<template>
  <v-dialog
    v-model="openLocal"
    :fullscreen="$vuetify.breakpoint.smAndDown"
    max-width="1100"
    scrollable
  >
    <v-card>
      <v-toolbar flat>
        <v-btn icon @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>

        <v-toolbar-title>{{ dialogTitle }}</v-toolbar-title>
        <v-spacer />

        <v-btn
          color="primary"
          :disabled="!selectedImage"
          @click="confirmSelection"
        >
          Usar imagen seleccionada
        </v-btn>
      </v-toolbar>

      <v-card-text class="picker-dialog__body">
        <v-row>
          <v-col cols="12" md="9">
            <div class="d-flex align-center mb-4">
              <div>
                <div class="text-subtitle-1 font-weight-medium">
                  Imágenes disponibles
                </div>
                <div class="text-caption text--secondary">
                  {{ helperText }}
                </div>
              </div>
              <v-spacer />
              <v-chip small outlined color="primary" class="mr-2">
                {{ filteredImages.length }} resultado(s)
              </v-chip>
              <v-btn small outlined :loading="loading" @click="fetchImages">
                <v-icon left small>mdi-refresh</v-icon>
                Actualizar
              </v-btn>
            </div>

            <v-row dense class="mb-2">
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="search"
                  dense
                  outlined
                  hide-details
                  clearable
                  prepend-inner-icon="mdi-magnify"
                  label="Buscar por nombre"
                />
              </v-col>

              <v-col cols="12" sm="6" md="3">
                <v-select
                  v-model="sortBy"
                  :items="sortItems"
                  dense
                  outlined
                  hide-details
                  label="Ordenar"
                />
              </v-col>

              <v-col cols="12" sm="6" md="3" class="d-flex justify-end">
                <v-btn-toggle
                  v-model="viewMode"
                  dense
                  mandatory
                  class="density-toggle"
                >
                  <v-tooltip bottom>
                    <template #activator="{ on, attrs }">
                      <v-btn
                        small
                        icon
                        value="comfortable"
                        v-bind="attrs"
                        v-on="on"
                      >
                        <v-icon small>mdi-view-grid-outline</v-icon>
                      </v-btn>
                    </template>
                    <span>Vista cómoda</span>
                  </v-tooltip>

                  <v-tooltip bottom>
                    <template #activator="{ on, attrs }">
                      <v-btn
                        small
                        icon
                        value="compact"
                        v-bind="attrs"
                        v-on="on"
                      >
                        <v-icon small>mdi-view-grid-plus-outline</v-icon>
                      </v-btn>
                    </template>
                    <span>Vista compacta</span>
                  </v-tooltip>
                </v-btn-toggle>
              </v-col>
            </v-row>

            <v-row dense class="mb-2">
              <v-col cols="12">
                <v-checkbox
                  v-model="onlyRecent"
                  hide-details
                  dense
                  class="mt-0 pt-0 only-recent-checkbox"
                  label="Solo imágenes de los últimos 30 días"
                />
              </v-col>
            </v-row>

            <div v-if="hasActiveFilters" class="mb-3 d-flex align-center">
              <div class="text-caption text--secondary mr-3">
                Filtros activos
              </div>
              <v-btn x-small text color="primary" @click="clearFilters">
                Limpiar filtros
              </v-btn>
            </div>

            <v-alert v-if="fetchError" type="error" dense outlined class="mb-4">
              {{ fetchError }}
            </v-alert>

            <v-row v-if="loading" dense>
              <v-col v-for="n in 4" :key="n" cols="6" md="3">
                <v-skeleton-loader type="image" />
              </v-col>
            </v-row>

            <v-row v-else dense>
              <v-col
                v-for="image in filteredImages"
                :key="image.url"
                cols="6"
                :md="imageCardMd"
              >
                <button
                  type="button"
                  class="picker-card"
                  :class="{
                    'picker-card--selected': isSelected(image),
                    'picker-card--compact': viewMode === 'compact',
                  }"
                  @click="selectImage(image)"
                  @dblclick="confirmImage(image)"
                >
                  <v-img
                    :src="image.url"
                    :lazy-src="image.url"
                    aspect-ratio="1"
                    class="picker-card__image"
                    contain
                  />

                  <div class="picker-card__meta">
                    <div class="picker-card__name" :title="image.name">
                      {{ image.name }}
                    </div>
                    <div class="picker-card__subtitle">
                      {{ formatModifiedAt(image.modified_at) }}
                    </div>
                  </div>

                  <div v-if="isSelected(image)" class="picker-card__check">
                    <v-icon color="white" small>mdi-check</v-icon>
                  </div>
                </button>
              </v-col>

              <v-col v-if="!filteredImages.length" cols="12">
                <v-sheet
                  outlined
                  rounded
                  class="pa-6 text-center text--secondary"
                >
                  {{ emptyStateComputed }}
                </v-sheet>
              </v-col>
            </v-row>
          </v-col>

          <v-col cols="12" md="3">
            <v-sheet outlined rounded class="pa-4 picker-sidebar">
              <div class="text-subtitle-1 font-weight-medium mb-2">
                Vista previa
              </div>

              <v-sheet
                outlined
                rounded
                class="picker-preview d-flex align-center justify-center mb-4"
              >
                <v-img
                  v-if="selectedImage"
                  :src="selectedImage.url"
                  contain
                  height="220"
                  width="100%"
                />
                <div
                  v-else
                  class="text-caption text--secondary text-center px-4"
                >
                  Selecciona una imagen existente o sube una nueva para verla
                  aquí.
                </div>
              </v-sheet>

              <v-sheet v-if="selectedImage" outlined rounded class="pa-3 mb-4">
                <div class="text-body-2 font-weight-medium text-truncate">
                  {{ selectedImage.name }}
                </div>
                <div class="text-caption text--secondary mb-2">
                  {{ formatModifiedAt(selectedImage.modified_at) }}
                </div>
                <div class="d-flex align-center">
                  <v-btn x-small text color="primary" @click="copySelectedUrl">
                    <v-icon left x-small>mdi-content-copy</v-icon>
                    Copiar URL
                  </v-btn>
                  <v-btn
                    x-small
                    text
                    color="grey darken-1"
                    @click="selectedImage = null"
                  >
                    Limpiar
                  </v-btn>
                </div>
              </v-sheet>

              <div class="text-subtitle-1 font-weight-medium mb-2">
                Cargar imagen local
              </div>

              <div
                class="upload-dropzone mb-3"
                :class="{ 'upload-dropzone--active': dragOver }"
                @click="openFileDialog"
                @dragenter.prevent="dragOver = true"
                @dragover.prevent="dragOver = true"
                @dragleave.prevent="dragOver = false"
                @drop.prevent="handleDrop"
              >
                <v-icon color="primary" large>mdi-cloud-upload-outline</v-icon>
                <div class="text-body-2 font-weight-medium mt-2">
                  Arrastra la imagen aquí
                </div>
                <div class="text-caption text--secondary mt-1">
                  o haz clic para buscarla
                </div>
                <div class="text-caption text--secondary mt-3">
                  PNG, JPG, JPEG, WEBP o SVG. Recomendado: 500 KB a 5 MB.
                </div>
                <div class="text-caption text--secondary mt-1">
                  Tamaño sugerido: {{ suggestedDimensions }}
                </div>
                <input
                  ref="fileInput"
                  type="file"
                  class="d-none"
                  accept="image/png,image/jpeg,image/webp,image/svg+xml"
                  @change="onFileInputChange"
                />
              </div>

              <v-alert
                v-if="uploadError"
                type="error"
                dense
                outlined
                class="mb-3"
              >
                {{ uploadError }}
              </v-alert>

              <v-alert
                v-if="uploadSuccess"
                type="success"
                dense
                outlined
                class="mb-3"
              >
                {{ uploadSuccess }}
              </v-alert>

              <v-sheet v-if="queuedFile" outlined rounded class="pa-3 mb-3">
                <div class="d-flex align-center mb-3">
                  <div class="flex-grow-1 mr-3">
                    <div class="text-body-2 font-weight-medium text-truncate">
                      {{ queuedFile.name }}
                    </div>
                    <div class="text-caption text--secondary">
                      {{ queuedFileSizeLabel }}
                    </div>
                  </div>
                  <v-btn
                    icon
                    small
                    :disabled="uploading"
                    @click="clearQueuedFile"
                  >
                    <v-icon small>mdi-close</v-icon>
                  </v-btn>
                </div>

                <v-img
                  v-if="queuedFilePreviewUrl"
                  :src="queuedFilePreviewUrl"
                  contain
                  max-height="180"
                  class="mb-3"
                />

                <v-progress-linear
                  v-if="uploading"
                  :value="uploadProgress"
                  color="primary"
                  height="8"
                  rounded
                  class="mb-3"
                />

                <v-btn
                  block
                  color="primary"
                  :loading="uploading"
                  :disabled="!queuedFile || uploading"
                  @click="uploadQueuedFile"
                >
                  Subir y usar imagen
                </v-btn>
              </v-sheet>
            </v-sheet>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
const allowedExtensions = ['png', 'jpg', 'jpeg', 'webp', 'svg']
const maxFileSizeBytes = 5 * 1024 * 1024

export default {
  name: 'ImagePickerDialog',

  props: {
    value: { type: Boolean, default: false },
    assetType: {
      type: String,
      required: true,
      validator(value) {
        return ['logos', 'covers'].includes(value)
      },
    },
  },

  data() {
    return {
      openLocal: this.value,
      images: [],
      loading: false,
      fetchError: '',
      search: '',
      sortBy: 'recent_desc',
      onlyRecent: false,
      viewMode: 'comfortable',
      selectedImage: null,
      dragOver: false,
      queuedFile: null,
      queuedFilePreviewUrl: '',
      uploadError: '',
      uploadSuccess: '',
      uploading: false,
      uploadProgress: 0,
    }
  },

  computed: {
    dialogTitle() {
      return this.assetType === 'logos'
        ? 'Seleccionar logo'
        : 'Seleccionar imagen de portada'
    },

    helperText() {
      return this.assetType === 'logos'
        ? 'Haz clic para seleccionar un logo o doble clic para usarlo de inmediato.'
        : 'Haz clic para seleccionar un fondo o doble clic para usarlo de inmediato.'
    },

    sortItems() {
      return [
        { text: 'Más recientes', value: 'recent_desc' },
        { text: 'Más antiguas', value: 'recent_asc' },
        { text: 'Nombre A-Z', value: 'name_asc' },
        { text: 'Nombre Z-A', value: 'name_desc' },
      ]
    },

    emptyStateText() {
      return this.assetType === 'logos'
        ? 'Aún no hay logos cargados en la biblioteca.'
        : 'Aún no hay fondos cargados en la biblioteca.'
    },

    emptyStateComputed() {
      if (!this.images.length) return this.emptyStateText
      return 'No hay resultados para los filtros aplicados.'
    },

    endpoint() {
      return `/catalog/api/assets/${this.assetType}/`
    },

    imageCardMd() {
      return this.viewMode === 'compact' ? 2 : 3
    },

    suggestedDimensions() {
      return this.assetType === 'logos' ? '600x200 px' : '1600x900 px'
    },

    hasActiveFilters() {
      return Boolean((this.search || '').trim()) || this.onlyRecent
    },

    filteredImages() {
      let out = [...this.images]
      const q = (this.search || '').trim().toLowerCase()

      if (q) {
        out = out.filter((image) =>
          (image.name || '').toLowerCase().includes(q)
        )
      }

      if (this.onlyRecent) {
        const now = Date.now()
        const days30 = 30 * 24 * 60 * 60 * 1000
        out = out.filter((image) => {
          const ms = Date.parse(image.modified_at || '')
          return Number.isFinite(ms) && now - ms <= days30
        })
      }

      out.sort((a, b) => {
        const an = (a.name || '').toLowerCase()
        const bn = (b.name || '').toLowerCase()
        const am = Date.parse(a.modified_at || '') || 0
        const bm = Date.parse(b.modified_at || '') || 0

        if (this.sortBy === 'name_asc') return an.localeCompare(bn)
        if (this.sortBy === 'name_desc') return bn.localeCompare(an)
        if (this.sortBy === 'recent_asc') return am - bm
        return bm - am
      })

      return out
    },

    queuedFileSizeLabel() {
      if (!this.queuedFile) return ''

      const sizeInKb = this.queuedFile.size / 1024
      if (sizeInKb < 1024) {
        return `${sizeInKb.toFixed(0)} KB`
      }

      return `${(sizeInKb / 1024).toFixed(2)} MB`
    },
  },

  watch: {
    value(value) {
      this.openLocal = value
      if (value) {
        this.onOpen()
      }
    },

    openLocal(value) {
      this.$emit('input', value)
      if (value) {
        this.onOpen()
      }
    },
  },

  beforeDestroy() {
    this.revokeQueuedPreview()
  },

  methods: {
    async onOpen() {
      this.fetchError = ''
      this.uploadError = ''
      this.uploadSuccess = ''
      this.search = ''
      this.sortBy = 'recent_desc'
      this.onlyRecent = false
      this.viewMode = 'comfortable'
      this.clearQueuedFile()
      this.selectedImage = null
      await this.fetchImages()
    },

    async fetchImages() {
      if (this.loading) return

      this.loading = true
      this.fetchError = ''

      try {
        const response = await this.$axios.$get(this.endpoint)
        this.images = Array.isArray(response && response.results)
          ? response.results
          : []
      } catch (error) {
        this.images = []
        this.fetchError =
          (error.response &&
            error.response.data &&
            error.response.data.detail) ||
          'No fue posible cargar la biblioteca de imágenes.'
      } finally {
        this.loading = false
      }
    },

    isSelected(image) {
      return Boolean(this.selectedImage && this.selectedImage.url === image.url)
    },

    selectImage(image) {
      this.selectedImage = image
      this.uploadError = ''
      this.uploadSuccess = ''
    },

    confirmImage(image) {
      this.selectedImage = image
      this.confirmSelection()
    },

    confirmSelection() {
      if (!this.selectedImage) return

      this.$emit('select', this.selectedImage.url)
      this.close()
    },

    close() {
      this.openLocal = false
    },

    openFileDialog() {
      if (this.uploading) return
      this.$refs.fileInput && this.$refs.fileInput.click()
    },

    clearFilters() {
      this.search = ''
      this.onlyRecent = false
    },

    formatModifiedAt(value) {
      const ms = Date.parse(value || '')
      if (!Number.isFinite(ms)) return 'Fecha no disponible'

      return new Date(ms).toLocaleString('es-EC', {
        year: 'numeric',
        month: 'short',
        day: '2-digit',
      })
    },

    async copySelectedUrl() {
      if (!this.selectedImage || !this.selectedImage.url) return

      try {
        await navigator.clipboard.writeText(this.selectedImage.url)
        this.uploadSuccess = 'URL copiada al portapapeles.'
      } catch (error) {
        this.uploadError = 'No se pudo copiar la URL automáticamente.'
      }
    },

    onFileInputChange(event) {
      const file = event.target && event.target.files && event.target.files[0]
      this.queueFile(file)

      if (event.target) {
        event.target.value = ''
      }
    },

    handleDrop(event) {
      this.dragOver = false
      const file =
        event.dataTransfer && event.dataTransfer.files
          ? event.dataTransfer.files[0]
          : null
      this.queueFile(file)
    },

    queueFile(file) {
      if (!file) return

      this.uploadError = ''
      this.uploadSuccess = ''

      const validationMessage = this.validateFile(file)
      if (validationMessage) {
        this.clearQueuedFile()
        this.uploadError = validationMessage
        return
      }

      this.revokeQueuedPreview()
      this.queuedFile = file
      this.queuedFilePreviewUrl = URL.createObjectURL(file)
    },

    validateFile(file) {
      const extension = ((file.name || '').split('.').pop() || '').toLowerCase()

      if (!allowedExtensions.includes(extension)) {
        return 'Formato no permitido. Usa PNG, JPG, JPEG, WEBP o SVG.'
      }

      if (file.size > maxFileSizeBytes) {
        return 'La imagen no puede exceder 5 MB.'
      }

      return ''
    },

    clearQueuedFile() {
      this.queuedFile = null
      this.uploadProgress = 0
      this.revokeQueuedPreview()
    },

    revokeQueuedPreview() {
      if (!this.queuedFilePreviewUrl) return

      URL.revokeObjectURL(this.queuedFilePreviewUrl)
      this.queuedFilePreviewUrl = ''
    },

    async uploadQueuedFile() {
      if (!this.queuedFile || this.uploading) return

      this.uploadError = ''
      this.uploadSuccess = ''
      this.uploading = true
      this.uploadProgress = 0

      const formData = new FormData()
      formData.append('file', this.queuedFile)

      try {
        const response = await this.$axios.post(this.endpoint, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          onUploadProgress: (event) => {
            if (!event.total) return
            this.uploadProgress = Math.round((event.loaded * 100) / event.total)
          },
        })

        const uploadedImage = response && response.data ? response.data : null
        if (!uploadedImage || !uploadedImage.url) {
          throw new Error('La respuesta del servidor no incluyó la URL final.')
        }

        this.uploadSuccess = 'Imagen cargada correctamente.'
        await this.fetchImages()
        this.selectedImage = uploadedImage
        this.$emit('select', uploadedImage.url)
        this.close()
      } catch (error) {
        this.uploadError =
          (error.response &&
            error.response.data &&
            error.response.data.detail) ||
          error.message ||
          'No fue posible subir la imagen.'
      } finally {
        this.uploading = false
      }
    },
  },
}
</script>

<style scoped>
.picker-dialog__body {
  background: linear-gradient(180deg, #faf7f1 0%, #ffffff 100%);
}

.picker-sidebar {
  position: sticky;
  top: 0;
  background: radial-gradient(
      circle at top left,
      rgba(0, 121, 107, 0.08),
      transparent 45%
    ),
    #ffffff;
}

.picker-preview {
  min-height: 240px;
  background: linear-gradient(
      135deg,
      rgba(0, 121, 107, 0.08),
      rgba(255, 255, 255, 0.92)
    ),
    #f8f8f8;
}

.picker-card {
  position: relative;
  width: 100%;
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 16px;
  overflow: hidden;
  background: #ffffff;
  cursor: pointer;
  transition: transform 0.18s ease, box-shadow 0.18s ease,
    border-color 0.18s ease;
}

.picker-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
}

.picker-card--selected {
  border-color: #00796b;
  box-shadow: 0 14px 28px rgba(0, 121, 107, 0.2);
}

.picker-card__image {
  background: linear-gradient(
      135deg,
      rgba(0, 121, 107, 0.08),
      rgba(255, 255, 255, 0.92)
    ),
    #f7f7f7;
}

.picker-card__meta {
  padding: 12px;
}

.picker-card--compact .picker-card__meta {
  padding: 8px;
}

.picker-card--compact .picker-card__name {
  font-size: 0.77rem;
}

.picker-card--compact .picker-card__subtitle {
  font-size: 0.68rem;
}

.picker-card__name {
  font-size: 0.82rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #24323d;
}

.picker-card__subtitle {
  font-size: 0.73rem;
  margin-top: 4px;
  color: #63717a;
}

.picker-card__check {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: #00796b;
}

.density-toggle {
  width: 100%;
  justify-content: flex-end;
}

.only-recent-checkbox {
  max-width: 320px;
}

.upload-dropzone {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  padding: 20px;
  border: 2px dashed rgba(0, 121, 107, 0.35);
  border-radius: 18px;
  background: linear-gradient(
      135deg,
      rgba(0, 121, 107, 0.06),
      rgba(255, 248, 235, 0.8)
    ),
    #ffffff;
  cursor: pointer;
  transition: border-color 0.18s ease, transform 0.18s ease,
    box-shadow 0.18s ease;
}

.upload-dropzone:hover,
.upload-dropzone--active {
  border-color: #00796b;
  transform: translateY(-1px);
  box-shadow: 0 12px 24px rgba(0, 121, 107, 0.12);
}
</style>
