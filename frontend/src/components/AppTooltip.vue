<template>
  <div>
    <a :id="'tooltip-' + key" class="tooltip-anchor" title="Incompatible browser" v-on:click="openTooltip" :style="{ 'font-size': anchor_size }">
      <icon :name="this.icon"></icon>
    </a>
    <div id="template" style="display: none;">
      <span>Empty</span>
    </div>
  </div>
</template>

<script>
  import Tippy from 'tippy.js'
  import Vue from 'vue'
  import bus from '@/utils/bus'

  var anchorKey
  var iconName
  var tooltipPosition
  var arrow
  var arrowSize
  var tooltipOffset
  var anchorFontSize

  var triggerTooltip = function () {
    let [emission, resourceUrl, modalHeader, recordId] = this.getAttribute('action').split(',')
    bus.$emit(emission, recordId, modalHeader, resourceUrl)
    bus.$emit('hide-tooltip', this.parentElement.children)
  }

  var addHandlers = function () {
    setTimeout(function () {
      var tooltipChildren = document.getElementsByClassName('tippy-tooltip-content')[0].children
      for (var i = 0; i < tooltipChildren.length; i++) {
        let child = tooltipChildren[i]
        if (child.nodeName === 'BUTTON') {
          child.addEventListener('click', triggerTooltip)
        }
      }
    }, 500)
  }

  var removeHandlers = function (tooltipChildren) {
    for (var i = 0; i < tooltipChildren.length; i++) {
      let child = tooltipChildren[i]
      if (child.nodeName === 'BUTTON') {
        child.removeEventListener('click', triggerTooltip)
      }
    }
  }

  Vue.directive('tooltip', {
    bind: function (el, binding) {
      anchorKey = binding.value.key || 0
      iconName = binding.value.icon || 'ellipsis-h'
      tooltipPosition = binding.value.position || 'right'
      arrow = binding.value.arrow || true
      arrowSize = binding.value.arrow_size || 'regular'
      tooltipOffset = binding.value.offset || 0
      anchorFontSize = binding.value.icon_size || '15px'
    }
  })

  export default {
    data: function () {
      return {
        tooltip: {},
        key: anchorKey,
        icon: iconName,
        anchor_size: anchorFontSize,
        tippy: null,
        open_tooltip: false
      }
    },
    mounted: function () {
      this.tippy = new Tippy('#tooltip-' + this.key, {
        html: this.tooltipTemplate || '#template',
        trigger: 'click',
        position: tooltipPosition,
        arrow: arrow,
        arrowSize: arrowSize,
        offset: tooltipOffset,
        animation: 'shift',
        interactive: true,
        size: 'big',
        theme: 'light',
        appendTo: document.querySelector('#app')
      })
      this.tippy
    },
    methods: {
      getPopper: function () {
        var tippyRef = document.querySelector('#tooltip-' + this.key)
        var popper
        if (tippyRef) {
          popper = this.tippy.getPopperElement(tippyRef)
        } else {
          popper = null
        }
        return popper
      },
      openTooltip: function () {
        this.open_tooltip = true
        addHandlers()
      },
      closeTooltip: function (tooltipChildren) {
        this.open_tooltip = false
        removeHandlers(tooltipChildren)
        var popper = this.getPopper()
        if (popper) {
          this.tippy.hide(popper)
        }
      }
    },
    created: function () {
      bus.$on('hide-tooltip', function (tooltipContentChildren) {
        this.closeTooltip(tooltipContentChildren)
      }.bind(this))
    },
    computed: {
      tooltipTemplate: function () {
        return this.$parent.$refs['tooltip-template-' + this.key] instanceof HTMLElement ? this.$parent.$refs['tooltip-template-' + this.key] : this.$parent.$refs['tooltip-template-' + this.key][0]
      }
    }
  }
</script>

<style scoped>
</style>
