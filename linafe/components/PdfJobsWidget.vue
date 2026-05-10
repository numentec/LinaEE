<template>
  <div class="pdf-widget">
    <v-btn small @click="open = !open"> PDFs ({{ jobs.length }}) </v-btn>

    <v-dialog v-model="open" max-width="520">
      <v-card>
        <v-card-title>Generación de PDF</v-card-title>
        <v-card-text>
          <div v-if="!jobs.length">No hay tareas activas.</div>

          <div v-for="j in jobs" :key="j.jobId" style="margin-bottom: 12px">
            <div style="display: flex; justify-content: space-between">
              <div>
                <b>Catálogo {{ j.catalogId }}</b>
              </div>
              <div>{{ j.status }}</div>
            </div>

            <v-progress-linear :value="j.progress" height="8" />
            <div style="font-size: 12px; color: #666; margin-top: 4px">
              {{ j.isEstimated ? 'Progreso estimado' : 'Progreso real' }}
            </div>
            <div style="margin-top: 8px">
              <v-btn
                v-if="j.status === 'queued' || j.status === 'running'"
                x-small
                text
                color="error"
                @click="cancelJob(j.jobId)"
              >
                Cancelar
              </v-btn>
            </div>
          </div>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn text @click="open = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  data: () => ({ open: false }),
  computed: {
    jobs() {
      return this.$store.getters['catalogo/catalogos/pdfJobsActive']
    },
  },
  methods: {
    async cancelJob(jobId) {
      if (!jobId) return
      await this.$store.dispatch('catalogo/catalogos/exportPdfCancel', {
        jobId,
      })
    },
  },
}
</script>

<style scoped>
.pdf-widget {
  position: fixed;
  right: 16px;
  bottom: 16px;
  z-index: 9999;
}
</style>
