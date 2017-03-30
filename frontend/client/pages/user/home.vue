<template>
  <div class="col-lg-10 col-lg-push-2 col-md-9 col-md-push-2 col-sm-8 col-sm-push-4 col-xs-12">
    <page-header></page-header>
    <div class="panel-group">
      <div v-for="panel in panels" class="col-lg-6 col-md-6 col-sm-6">
        <base-panel :panel="panel" :key="panel.key"></base-panel>
      </div>
    </div>
  </div>
</template>

<script>
  import PageHeader from '~components/PageHeader.vue'
  import BasePanel from '~components/BasePanel.vue'
  export default {
    layout: 'dashboard',
    components: {
      PageHeader: PageHeader,
      BasePanel: BasePanel
    },
    data: function () {
      return {
        panels: [
          {name: 'add_relative_panel', open: false, label: 'Add Relative', icon: 'fa fa-user-plus fa-fw', key: 1},
          {name: 'add_relationship_panel', open: false, label: 'Add Relationship', icon: 'fa fa-link fa-fw', key: 2}
        ]
      }
    }
  }
</script>

<style scoped>
  .panel-group {
    margin: 20px
  }
</style>
