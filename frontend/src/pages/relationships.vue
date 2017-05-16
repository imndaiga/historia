<template>
  <app-table resource_url="/api/relationships"></app-table>
</template>

<script>
  import AppTable from '@/components/AppTable'
  export default {
    components: {
      AppTable: AppTable
    }
  }
</script>

<style scoped>
</style>
