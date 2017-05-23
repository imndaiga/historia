<template>
  <div>
    <a :id="'tooltip-' + key" class="tooltip-anchor" title="Incompatible browser" v-on:click="setUpTooltip">
      <icon name="ellipsis-h"></icon>
    </a>
    <div id="template" style="display: none;">
      <span>Empty</span>
    </div>
  </div>
</template>

<script>
  import Tippy from 'tippy.js'
  import bus from '@/utils/bus'

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
        key: this.anchor_key,
        tippy: {}
      }
    },
    mounted: function () {
      this.tippy = new Tippy('#tooltip-' + this.key, {
        html: this.$parent.$refs['tooltip-template-' + this.key][0] || '#template',
        trigger: 'click',
        position: 'left',
        animation: 'shift',
        arrow: true,
        arrowSize: 'small',
        interactive: true,
        size: 'big',
        theme: 'light',
        appendTo: document.querySelector('#app')
      })
      this.tippy
    },
    methods: {
      setUpTooltip: function () {
        bus.$emit('set-up-tooltip')
      }
    },
    created: function () {
      bus.$on('modal-data-ready', function () {
        var popper = this.tippy.getPopperElement(document.querySelector('#tooltip-' + this.key))
        this.tippy.hide(popper)
      }.bind(this))
    }
  }
</script>

<style>
  .tippy-popper {
    border: none;
    outline: none
  }
  .tooltip-anchor,
  .tooltip-anchor:focus,
  .tooltip-anchor:hover {
    color: grey
  }
</style>
