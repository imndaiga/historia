<template>
  <div>
    <nuxt/>
    <alert-message></alert-message>
  </div>
</template>

<script>
  import AlertMessage from '~components/AlertMessage.vue'
  export default {
    components: {
      AlertMessage: AlertMessage
    },
    created: function () {
      if (this.$http) {
        this.$http.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('id_token')
      }
    }
  }
</script>

<style>
</style>
