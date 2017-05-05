<template>
  <div class="hidden-lg hidden-md hidden-sm header">
    <a v-on:click="openMobileMenu" class="header-title">
      <icon name="bars"></icon>
      {{current_Panel}}
    </a>
  </div>
</template>

<script>
  import bus from '../bus'
  export default {
    methods: {
      openMobileMenu: function () {
        bus.$emit('open-mobile-menu')
      }
    },
    computed: {
      current_Panel: function () {
        return this.$route.name
      }
    }
  }
</script>

<style scoped>
  .header {
    position: relative;
    padding-bottom: 15px;
    padding-top: 20px;
    border-bottom: 1px solid #eee;
    text-indent: 50px;
  }
  .header > a > .fa-icon{
    position: absolute;
    left: 20px;
    top: 33px;
  }
  .header > a,
  .header > a:hover,
  .header > a:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
  }
  .header-title {
    font-size: 30px;
    margin-left: 10%;
    text-transform: capitalize;
  }
</style>
