<template>
  <div class="hidden-lg hidden-md hidden-sm page-menu-header">
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
    position: relative;
    padding-bottom: 15px;
    padding-top: 20px;
    border-bottom: 1px solid #eee;
    text-indent: 50px
  }
  .page-menu-header > button {
    position: absolute;
    left: 10px;
    top: 18px;
    border: none
  }
  .page-menu-title {
    font-size: 30px;
    margin-left: 10%;
    text-transform: capitalize
  }
</style>
