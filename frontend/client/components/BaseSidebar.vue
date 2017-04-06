<template>
  <div class="col-lg-2 col-md-3 col-sm-4 sidebar">
    <hook-app-menu :pages="pages" :footer="footer"></hook-app-menu>
  </div>
</template>

<script>
  import HookAppMenu from '~components/HookAppMenu.vue'
  export default {
    components: {
      HookAppMenu: HookAppMenu
    },
    props: {
      pages: {
        type: Array,
        required: true
      },
      footer: {
        type: Array,
        required: true
      }
    }
  }
</script>

<style scoped>
  .sidebar {
    position: fixed;
    top: 0;
    height: 100%;
    left: 0;
    z-index: 1000;
    display: block;
    padding: 20px;
    overflow-x: hidden;
    overflow-y: auto; /* Scrollable contents if viewport is shorter than content. */
    background-color: #f5f5f5;
    border-right: 1px solid #eee;
    padding-top: 20px
  }
</style>
