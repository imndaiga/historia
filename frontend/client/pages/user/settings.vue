<template>
  <div class="col-lg-10 col-lg-push-2 col-md-9 col-md-push-3 col-sm-8 col-sm-push-4 col-xs-12">
    <page-header></page-header>
  </div>
</template>

<script>
  import PageHeader from '~components/PageHeader.vue'
  export default {
    fetch: function ({ store, redirect }) {
      if (!store.state.authUser) {
        return redirect('/')
      }
    },
    layout: 'dashboard',
    components: {
      PageHeader: PageHeader
    }
  }
</script>

<style scoped>
</style>
