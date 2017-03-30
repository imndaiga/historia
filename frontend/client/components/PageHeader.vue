<template>
  <div class="hidden-lg hidden-md hidden-sm col-xs-12 page-menu-header">
    <button class="btn btn-default btn-lg" v-on:click="openMobileMenu">
      <span class="fa fa-bars fa-lg"></span>
    </button>
    <span class="page-menu-title">{{current_Panel}}</span>
  </div>
</template>

<script>
  export default {
    methods: {
      openMobileMenu: function () {
        this.$nuxt.$emit('open-mobile-menu')
      }
    },
    computed: {
      current_Panel: function () {
        return this.$nuxt.$route.name.split('-')[0]
      }
    }
  }
</script>

<style scoped>
  .page-menu-header {
    margin-bottom: 10px;
    padding-bottom: 15px;
    padding-top: 20px;
    border-bottom: 1px solid #eee;
    text-indent: 50px
  }
  .page-menu-header > button {
    margin-top: -10px;
    margin-left: -50px
  }
  .page-menu-title {
    font-size: 30px;
    margin-left: 15px;
    text-transform: capitalize
  }
</style>
