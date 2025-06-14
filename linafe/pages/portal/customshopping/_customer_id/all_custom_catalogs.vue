<template>
  <div>
    <h1>All Custom Catalogs</h1>
    <p>
      Here you can view all custom catalogs for {{ $route.params.customer_id }}.
    </p>
    <p>Use the navigation drawer to access different sections.</p>
    <p>Click on a catalog to view its details.</p>
  </div>
</template>

<script>
export default {
  name: 'AllCustomCatalogs',
  layout: 'publicapps',
}
</script>

<style lang="scss" scoped></style>
