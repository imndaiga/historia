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
    }
  }
</script>

<style>
</style>
