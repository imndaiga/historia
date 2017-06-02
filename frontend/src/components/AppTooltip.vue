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

  var anchorKey
  var iconName
  var tooltipPosition
  var arrow
  var arrowSize
  var tooltipOffset
  var anchorFontSize

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
        this.addHandlers()
      },
      closeTooltip: function (tooltipChildren) {
        this.open_tooltip = false
        this.removeHandlers(tooltipChildren)
        var popper = this.getPopper()
        if (popper) {
          this.tippy.hide(popper)
        }
      },
      triggerTooltip: function (element) {
        let [action, resourceUrl, modalHeader, recordId] = element.getAttribute('action').split(',')
        this.$emit('perform-action', action, recordId, modalHeader, resourceUrl)
        this.closeTooltip(element.parentElement.getElementsByTagName('button'))
      },
      addHandlers: function () {
        var self = this
        setTimeout(function () {
          var buttons = document.getElementsByClassName('tippy-tooltip-content')[0].getElementsByTagName('button')
          for (var i = 0; i < buttons.length; i++) {
            let button = buttons[i]
            button.addEventListener('click', function () {
              self.triggerTooltip(this)
            })
          }
        }, 500)
      },
      removeHandlers: function (tooltipChildren) {
        var self = this
        for (var i = 0; i < tooltipChildren.length; i++) {
          let child = tooltipChildren[i]
          if (child.nodeName === 'BUTTON') {
            child.removeEventListener('click', function () {
              self.triggerTooltip(this)
            })
          }
        }
      }
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
