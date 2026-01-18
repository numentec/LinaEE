<template>
  <v-card
    outlined
    class="h-100 d-flex flex-column"
    @click="$emit('open', item.id)"
  >
    <v-card-title class="d-flex align-start">
      <div class="text-subtitle-1 font-weight-medium" style="line-height: 1.2">
        {{ item.name }}
      </div>
      <v-spacer />
      <v-chip small :color="statusColor" text-color="white">
        {{ statusLabel }}
      </v-chip>
    </v-card-title>

    <v-card-subtitle class="pt-0">
      <div class="d-flex flex-wrap">
        <div class="mr-3">
          Plantilla: <strong>{{ item.template }}</strong>
        </div>
        <div class="mr-3">
          Páginas: <strong>{{ item.pages_count || 1 }}</strong>
        </div>
        <div>
          Orientación:
          <strong>{{
            item.orientation === 'portrait' ? 'Vertical' : 'Horizontal'
          }}</strong>
        </div>
      </div>
      <div class="mt-1 text--secondary">
        Actualizado: {{ formattedUpdatedAt }}
      </div>
    </v-card-subtitle>

    <v-spacer />

    <v-card-actions @click.stop>
      <v-btn small color="primary" @click="$emit('open', item.id)"
        >Editar</v-btn
      >
      <v-btn small text @click="$emit('duplicate', item.id)">Duplicar</v-btn>
      <v-btn small text @click="$emit('share', item.id)">Compartir</v-btn>

      <v-spacer />

      <v-menu left bottom>
        <template #activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>
        <v-list dense>
          <v-list-item @click="$emit('exportPdf', item.id)">
            <v-list-item-title>Exportar PDF</v-list-item-title>
          </v-list-item>
          <v-list-item @click="$emit('archive', item.id)">
            <v-list-item-title>Archivar</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'CatalogCard',
  props: {
    item: { type: Object, required: true },
  },
  computed: {
    statusLabel() {
      const map = {
        draft: 'Borrador',
        ready: 'Listo',
        sent: 'Enviado',
        expired: 'Expirado',
        archived: 'Archivado',
      }
      return map[this.item.status] || this.item.status
    },
    statusColor() {
      const map = {
        draft: 'grey',
        ready: 'blue',
        sent: 'green',
        expired: 'orange',
        archived: 'brown',
      }
      return map[this.item.status] || 'grey'
    },
    formattedUpdatedAt() {
      try {
        const d = new Date(this.item.updated_at)
        return d.toLocaleString()
      } catch (e) {
        return this.item.updated_at
      }
    },
  },
}
</script>
