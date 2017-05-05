<template>
  <actions-bar :title="actions_bar_title" :buttons="action_buttons"></actions-bar>
</template>

<script>
  import AppActionsBar from '@/components/AppActionsBar.vue'
  export default {
    components: {
      ActionsBar: AppActionsBar
    },
    data: function () {
      return {
        actions_bar_title: 'Quick Actions',
        action_buttons: [
          {
            message: 'Add Relative',
            icon: 'user-plus',
            action: 'open_add_relative_modal',
            key: 1
          },
          {
            message: 'Add Relationship',
            icon: 'link',
            action: 'open_add_relation_modal',
            key: 2
          }
        ]
      }
    }
  }
</script>

<style scoped>
</style>
