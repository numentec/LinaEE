<template>
  <v-dialog :value="value" max-width="500" @input="$emit('input', $event)">
    <v-card>
      <v-toolbar flat>
        <v-btn icon @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Editar categoría</v-toolbar-title>
      </v-toolbar>

      <v-card-text>
        <v-file-input
          v-model="imageFile"
          label="Nueva imagen"
          accept="image/*"
          outlined
          show-size
          prepend-icon="mdi-camera"
          :rules="imageRules"
        />
        <v-text-field
          v-model.number="ordinal"
          label="Ordinal"
          type="number"
          outlined
          :rules="ordinalRules"
        />
        <v-alert v-if="errorMessage" type="error" dense>{{
          errorMessage
        }}</v-alert>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn text @click="close">Cancelar</v-btn>
        <v-btn color="primary" :loading="saving" @click="save">Guardar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
const MAX_IMAGE_SIZE = 5 * 1024 * 1024

export default {
  name: 'CategoryEditDialog',
  props: {
    value: {
      type: Boolean,
      default: false,
    },
    category: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      imageFile: null,
      ordinal: this.category.ordinal ?? 0,
      saving: false,
      errorMessage: '',
      imageRules: [
        (file) =>
          !file ||
          file.size <= MAX_IMAGE_SIZE ||
          'La imagen no debe superar 5 MB',
      ],
      ordinalRules: [
        (val) => (val !== null && val !== '') || 'El ordinal es requerido',
        (val) =>
          Number.isInteger(Number(val)) ||
          'El ordinal debe ser un número entero',
      ],
    }
  },
  watch: {
    value(isOpen) {
      // reinicia el formulario cada vez que se abre el diálogo
      if (isOpen) {
        this.imageFile = null
        this.ordinal = this.category.ordinal ?? 0
        this.errorMessage = ''
      }
    },
  },
  methods: {
    close() {
      this.$emit('input', false)
    },
    async save() {
      this.errorMessage = ''
      this.saving = true

      const formData = new FormData()
      formData.append('ordinal', this.ordinal)
      if (this.imageFile) {
        formData.append('image', this.imageFile)
      }

      try {
        const updated = await this.$store.dispatch(
          'shoppingcart/categories/updateCategory',
          { categoryId: this.category.id, formData }
        )
        this.$emit('updated', updated)
        this.close()
      } catch (error) {
        this.errorMessage = error.message
      } finally {
        this.saving = false
      }
    },
  },
}
</script>
