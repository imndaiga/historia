<template>
  <div>
    <a :id="'tooltip-' + key" class="tooltip-anchor" title="Incompatible browser">
      <icon name="ellipsis-h"></icon>
    </a>
    <div id="template" style="display: none;">
      <span>Empty</span>
    </div>
  </div>
</template>

<script>
  import Tippy from 'tippy.js'

  export default {
    props: {
      anchor_key: {
        required: true,
        type: Number
      }
    },
    data: function () {
      return {
        tooltip: {},
        key: this.anchor_key
      }
    },
    mounted: function () {
      const ref = document.getElementById('tooltip-' + this.key)
      var tippy = new Tippy(ref, {
        html: this.$parent.$refs['tooltip-template'][0] || '#template',
        trigger: 'click',
        position: 'left',
        animation: 'shift',
        arrow: true,
        arrowSize: 'small',
        interactive: true,
        size: 'big',
        theme: 'light',
        hideDelay: 300,
        appendTo: document.querySelector('#app')
      })
      tippy
    }
  }
</script>

<style scoped>
  .fa-icon {
    width: auto;
    height: 1.2em
  }
</style>
