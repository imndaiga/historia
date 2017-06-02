<template>
  <div>
    <a :id="'tooltip-' + anchorKey" class="tooltip-anchor" title="Incompatible browser" v-on:click="openTooltip" :style="{ 'font-size': iconSize }">
      <icon :name="icon"></icon>
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
      anchorKey: {
        required: true,
        type: Number
      },
      icon: {
        required: true,
        type: String
      },
      position: {
        required: false,
        type: String,
        default: 'right'
      },
      arrow: {
        required: false,
        type: Boolean,
        default: true
      },
      arrowSize: {
        required: false,
        type: String,
        default: 'regular'
      },
      offset: {
        required: false,
        type: Number,
        default: 0
      },
      iconSize: {
        required: false,
        type: String,
        default: '15px'
      }
    },
    data: function () {
      return {
        tooltip: {},
        tippy: null,
        open_tooltip: false
      }
    },
    mounted: function () {
      this.tippy = new Tippy('#tooltip-' + this.anchorKey, {
        html: this.tooltipTemplate || '#template',
        trigger: 'click',
        position: this.position,
        arrow: this.arrow,
        arrowSize: this.arrowSize,
        offset: this.offset,
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
        var tippyRef = document.querySelector('#tooltip-' + this.anchorKey)
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
        return this.$parent.$refs['tooltip-template-' + this.anchorKey] instanceof HTMLElement ? this.$parent.$refs['tooltip-template-' + this.anchorKey] : this.$parent.$refs['tooltip-template-' + this.anchorKey][0]
      }
    }
  }
</script>

<style scoped>
</style>
