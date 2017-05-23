<template>
  <div id="sigma-parent">
    <app-reload v-if="!graph_Is_Ready" message="No Relationship Data Available" v-on:reload-resource="forceReload"></app-reload>
    <div id="sigma-container" class="col-lg-12 col-md-12 col-sm-12 col-xs-12"></div>
    <div class="toolbox">
      <div ref="tooltip-template-1" class="tooltip-template">
        <button type="button" v-for="button in toolbar_actions" v-on:click="performAction(button.action)" :class="button.class" :title="button.title" :action="[button.action]">
          <icon :name="button.icon"></icon>
        </button>
      </div>
      <app-tooltip v-if="graph_Is_Ready" :anchor_key="1" anchor_icon="sliders" position="bottom"></app-tooltip>
    </div>
  </div>
</template>

<script>
  import 'sigma/build/sigma.min.js'
  import 'sigma/plugins/sigma.layout.forceAtlas2/supervisor.js'
  import 'sigma/plugins/sigma.layout.forceAtlas2/worker.js'
  import AppReload from '@/components/AppReload'
  import AppTooltip from '@/components/AppTooltip'
  import bus from '@/utils/bus'

  export default {
    components: {
      AppReload: AppReload,
      AppTooltip: AppTooltip
    },
    data: function () {
      return {
        graph: {},
        resource_url: '/api/graph',
        loading: false,
        s: { graph: '' },
        toolbar_actions: [
          {
            title: 'Play',
            action: 'play-forceatlas',
            class: 'btn btn-sm btn-default action-button',
            icon: 'play'
          },
          {
            title: 'Pause',
            action: 'pause-forceatlas',
            class: 'btn btn-sm btn-default action-button',
            icon: 'pause'
          }
        ]
      }
    },
    methods: {
      getData: function () {
        this.loading = true
        var self = this
        this.$http.get(this.resource_url)
        .then(
          function (response) {
            self.graph = response.data.graph
            self.renderGraph()
          }).catch(function (error) {
            console.log(error)
            bus.$emit('modal-data-ready', 'Ooops!', 'exclamation-circle', null, null, 'An error occured!', 'Something went wrong while retrieving data.', 'red')
          })
        this.loading = false
      },
      renderGraph: function () {
        var self = this
        var Sigma = window.sigma
        this.s = new Sigma({
          graph: this.graph,
          container: 'sigma-container',
          settings: {
            defaultLabelSize: 20,
            font: 'Open Sans',
            labelThreshold: 12
          }
        })
        this.s.startForceAtlas2({worker: true, barnesHutOptimize: false})
        setTimeout(function () {
          self.s.stopForceAtlas2()
        }, 500)
      },
      forceReload: function (data) {
        this.getData()
      }
    },
    computed: {
      graph_Is_Ready: function () {
        if (this.s.graph.nodes) {
          return true
        } else {
          return false
        }
      }
    },
    created: function () {
      this.getData()
      bus.$on('play-forceatlas', function () {
        this.s.startForceAtlas2({worker: true, barnesHutOptimize: false})
      }.bind(this))
      bus.$on('pause-forceatlas', function () {
        this.s.stopForceAtlas2()
      }.bind(this))
    }
  }
</script>

<style scoped>
  #sigma-parent {
    position: relative;
  }
  #sigma-container {
    position: absolute;
    height: 100vh;
    padding: 0;
  }
  .page-message {
    margin-top: 20%;
    font-size: 20px
  }
  .tooltip-template {
    display: none
  }
  .toolbox {
    position: absolute;
    z-index: 1000;
    margin: 3% 0 0 3%
  }
  .fa-icon {
    width: auto;
    height: 1em;
  }
  button {
    font-size: 15px;
  }
</style>
