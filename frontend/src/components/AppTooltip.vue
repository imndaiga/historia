<template>
  <div>
    <a :id="'tooltip-' + anchorKey" :class="['tooltip-anchor', anchorClass]" title="Incompatible browser" v-on:click="openTooltip" :style="{ 'font-size': iconSize }">
      <icon :name="icon"></icon>
    </a>
    <div id="default-template" style="display: none;">
      <span>Empty</span>
    </div>
    <slot name="template"></slot>
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
      anchorClass: {
        required: false,
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
        html: this.$slots.template[0].elm || '#default-template',
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
        this.addListeners()
      },
      closeTooltip: function () {
        this.open_tooltip = false
        var popper = this.getPopper()
        if (popper) {
          this.tippy.hide(popper)
        }
      },
      triggerTooltipAction: function (event) {
        var element = event.currentTarget
        let [action, resourceUrl, modalHeader, recordId] = element.getAttribute('action').split(',')
        this.$emit('perform-action', action, recordId, modalHeader, resourceUrl)
        this.removeListeners()
        this.closeTooltip()
      },
      addListeners: function () {
        var self = this
        setTimeout(function () {
          for (var i = 0; i < self.tooltipActors.length; i++) {
            let actor = self.tooltipActors[i]
            actor.addEventListener('click', self.triggerTooltipAction)
          }
        }, 500)
      },
      removeListeners: function () {
        var self = this
        for (var i = 0; i < this.tooltipActors.length; i++) {
          let actor = self.tooltipActors[i]
          actor.removeEventListener('click', self.triggerTooltipAction)
        }
      }
    },
    computed: {
      tooltipActors: function () {
        var tippyElements = document.getElementsByClassName('tippy-tooltip-content')
        return tippyElements.length > 0 ? tippyElements[0].getElementsByTagName('button') : []
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
