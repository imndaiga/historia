<template>
  <div>
    <a :id="'tooltip-' + key" class="tooltip-anchor" title="Incompatible browser" v-on:click="setUpTooltip">
      <icon :name="this.anchor_icon"></icon>
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
      },
      anchor_icon: {
        required: true,
        type: String
      },
      position: {
        required: true,
        type: String
      }
    },
    data: function () {
      return {
        tooltip: {},
        key: this.anchor_key,
        tippy: null
      }
    },
    mounted: function () {
      this.tippy = new Tippy('#tooltip-' + this.key, {
        html: this.tooltipTemplate || '#template',
        trigger: 'click',
        position: this.position,
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
        var tippyRef = document.querySelector('#tooltip-' + this.key)
        if (tippyRef) {
          var popper = this.tippy.getPopperElement(tippyRef)
          this.tippy.hide(popper)
        }
      }.bind(this))
    },
    computed: {
      tooltipTemplate: function () {
        return this.$parent.$refs['tooltip-template-' + this.key] instanceof HTMLElement ? this.$parent.$refs['tooltip-template-' + this.key] : this.$parent.$refs['tooltip-template-' + this.key][0]
      }
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
