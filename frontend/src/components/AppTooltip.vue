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
  import Vue from 'vue'
  import bus from '@/utils/bus'

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
    bind: function () {
      bus.$on('set-up-tooltip', function () {
        addHandlers()
      })
    }
  })

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
      bus.$on('hide-tooltip', function (tooltipContentChildren) {
        removeHandlers(tooltipContentChildren)
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
