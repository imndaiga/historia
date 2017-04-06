<template>
  <div v-if="open_mobile_menu" class="container-fluid">
    <div class="row">
      <div class="mobile-menu">
        <a v-on:click="closeMobileMenu">&times;</a>
        <hook-app-menu :pages="pages" :footer="footer"></hook-app-menu>
      </div>
    </div>
  </div>
</template>

<script>
  import HookAppMenu from '~components/HookAppMenu.vue'
  export default {
    components: {
      HookAppMenu: HookAppMenu
    },
    data: function () {
      return {
        open_mobile_menu: false
      }
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
    },
    methods: {
      closeMobileMenu: function () {
        document.getElementsByTagName('body')[0].classList.remove('stop-scrolling')
        this.open_mobile_menu = false
      },
      openMobileMenu: function () {
        document.getElementsByTagName('body')[0].classList.add('stop-scrolling')
        this.open_mobile_menu = true
      }
    },
    created: function () {
      this.$nuxt.$on('open-mobile-menu', function () {
        this.open_mobile_menu = true
      }.bind(this))
      this.$nuxt.$on('routeChanged', function () {
        document.getElementsByTagName('body')[0].classList.remove('stop-scrolling')
        this.open_mobile_menu = false
      }.bind(this))
    }
  }
</script>

<style scoped>
  .mobile-menu {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1001;
    display: block;
    padding: 20px;
    overflow-x: hidden;
    overflow-y: auto; /* Scrollable contents if viewport is shorter than content. */
    background-color: rgba(214, 214, 214, 0.9);
    border-right: 1px solid #eee;
    padding-top: 20px
  }
  .mobile-menu > a {
    position: absolute;
    top: 0;
    right: 25px;
    font-size: 36px;
    margin-left: 50px;
    text-decoration: none;
    cursor: pointer
  }
</style>
