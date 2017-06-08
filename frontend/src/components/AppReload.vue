<template>
  <div class="text-center">
    <p class="page-message">{{ load_message }}</p>
    <a v-on:click="reloadResource">
      <icon name="refresh"></icon>
      <span class="reload-text">Reload</span>
    </a>  
  </div>
</template>

<script>
  export default {
    props: {
      message: {
        required: true,
        type: String
      }
    },
    data: function () {
      return {
        load_message: this.message
      }
    },
    methods: {
      reloadResource: function () {
        this.$emit('reload-resource')
        this.$store.dispatch('forceMobileMenuExit')
        this.$store.dispatch('forceModalExit')
      }
    }
  }
</script>

<style scoped>
  .page-message {
    margin-top: 25%;
    font-size: 20px;
  }
  a {
    text-decoration: none;
    color: grey;
    cursor: pointer;
    font-size: 18px;
  }
  a:hover,
  a:focus {
    text-decoration: none;
    color: black;
  }
  .fa-icon {
    padding-top: 4px;
    margin-right: 5px;
  }
</style>
