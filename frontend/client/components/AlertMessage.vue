<template>
  <div v-if="alert_Is_Visible" :class="['alert', alert.type]">
    <a class="close" v-if="alert.dismissable" v-on:click="dismissMessage">&times;</a>
    <span v-html="alert.message"></span>
  </div>
</template>

<script>
  export default {
    methods: {
      dismissMessage: function () {
        this.$nuxt.$store.dispatch('dismiss_alert')
      }
    },
    computed: {
      alert: function () {
        if (this.$nuxt) {
          return this.$nuxt.$store.state.alert
        } else {
          return {}
        }
      },
      alert_Is_Visible: function () {
        var self = this
        if (Object.keys(this.alert).length > 0) {
          if (!this.alert.dismissable) {
            var timeout = this.$nuxt.$store.state.alert.duration === 0 ? 1500 : this.$nuxt.$store.state.alert.duration
            setTimeout(self.dismissMessage, timeout)
            return true
          } else {
            return true
          }
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
