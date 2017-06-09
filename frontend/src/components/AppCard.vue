<template>
  <div class="col-lg-3 col-md-4 col-sm-6 col-xs-6">
    <div class="panel panel-default" :style="panelStyle">
      <div v-if="displayHeader" class="panel-heading">
        <icon v-if="headerIcon" :name="headerIcon"></icon>
        <span v-if="header" class="header-text">{{ header }}</span>
      </div>
      <div class="panel-body" :style="bodyStyle">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      header: {
        type: String,
        required: false
      },
      headerIcon: {
        type: String,
        required: false
      },
      panelStyle: {
        type: String,
        required: false
      },
      bodyStyle: {
        type: String,
        required: false
      }
    },
    computed: {
      displayHeader: function () {
        return this.header && this.headerIcon
      }
    }
  }
</script>

<style scoped>
  .panel,
  .panel .panel-heading,
  .panel .panel-body {
    border-radius: 0px
  }
  .fa-icon {
    vertical-align: -4px
  }
  .panel-heading {
    font-size: 19px
  }
  .header-text {
    padding-left: 4%;
    font-weight: 600;
    font-size: 15px
  }
  .panel {
    min-height: 120px
  }
</style>
