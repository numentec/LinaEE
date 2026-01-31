<template>
  <div class="print-layout">
    <Nuxt />
  </div>
</template>

<script>
export default {
  name: 'PrintLayout',
  head() {
    return {
      title: 'Catálogo',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      ],
    }
  },
}
</script>

<style>
/* ============================= */
/* RESET TOTAL PARA IMPRESIÓN    */
/* ============================= */
html,
body {
  margin: 0;
  padding: 0;
  background: #fff;
}

.print-layout {
  background: #fff;
}

/* Evita scrollbars en Chromium */
body {
  overflow: hidden;
}
</style>
