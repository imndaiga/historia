<template>
  <div v-if="alert_Is_Visible" :class="['alert', alert_type, {'alert-dismissable': dismissable}]">
    <a class="close" v-if="dismissable" v-on:click="dismissMessage">&times;</a>
    <span v-html="message"></span>
  </div>
</template>

<script>
  export default {
    data: function () {
      return {
        alert_type: '',
        message: '',
        dismissable: true,
        timeout: 0,
        dismissed: false
      }
    },
    methods: {
      dismissMessage: function () {
        this.dismissed = true
      }
    },
    computed: {
      alert_Is_Visible: function () {
        if (this.message.length > 0 && !this.dismissable) {
          return true
        } else if (this.message.length > 0 && this.dismissable && !this.dismissed) {
          return true
        } else {
          return false
        }
      }
    }
  }
</script>

<style scoped>
  .alert {
    position: absolute;
    z-index: 1002;
    top: 10px;
    left: 40px;
    right: 40px;
    font-size: 18px;
    text-align: center;
    opacity: 0.9
  }
</style>
