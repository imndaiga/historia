<template>
  <div id="sigma-parent">
    <app-reload v-if="!graphHasData" message="No Relationship Data Available" v-on:reload-resource="forceReload"></app-reload>
    <div v-show="graphHasData">
      <div id="sigma-container" class="col-lg-12 col-md-12 col-sm-12 col-xs-12"></div>
      <div class="toolbox">
        <app-tooltip v-on:perform-action="performAction" :anchorKey="1" icon="sliders" position="bottom" :offset="120" iconSize="25px">
          <div slot="template" class="tooltip-template">
            <p class="tooltip-header">Toolbar</p>
            <p class="tooltip-info">Control Visualisation Parameters</p>
            <actions-bar title="Playback" :buttons="toolbar_actions" :styles="actions_bar_style"></actions-bar>
          </div>
        </app-tooltip>
      </div>
      <app-modal :header="modalData.header" :headerIcon="modalData.headerIcon" :submitMessage="modalData.submitMessage" :color="modalData.color" :type="modalData.type" :modalIsOpen="modalData.open">
        <div v-if="modalData.type === 'alert'">
          <p class="alert-header">{{ modalData.subject }}</p>
          <p class="alert-message" v-if="modalData.message.length > 0">{{ modalData.message }}</p>
        </div>
      </app-modal>
    </div>
  </div>
</template>

<script>
  import 'sigma/build/sigma.min.js'
  import 'sigma/plugins/sigma.layout.forceAtlas2/supervisor.js'
  import 'sigma/plugins/sigma.layout.forceAtlas2/worker.js'
  import AppReload from '@/components/AppReload'
  import AppTooltip from '@/components/AppTooltip'
  import AppActionsBar from '@/components/AppActionsBar'
  import { createModalData, errors } from '@/utils/helper'
  import AppModal from '@/components/AppModal'

  export default {
    components: {
      AppReload: AppReload,
      AppTooltip: AppTooltip,
      ActionsBar: AppActionsBar,
      AppModal: AppModal
    },
    data: function () {
      return {
        graph: {},
        resource_url: '/api/graph',
        s: { graph: '' },
        toolbar_actions: [
          {
            title: 'Play',
            action: 'play-forceatlas',
            message: 'Play',
            icon: 'play'
          },
          {
            title: 'Pause',
            action: 'pause-forceatlas',
            message: 'Pause',
            icon: 'pause'
          }
        ],
        actions_bar_style: {
          well: 'background-color: #fff; max-width: 300px',
          row: 'line-height: 22px; height: 22px',
          titleDivClass: 'col-lg-4 col-md-4 col-sm-5 hidden-xs',
          title: 'font-weight: 600; margin-left: 10px; font-size: 15px',
          buttonDivClass: 'col-lg-8 col-md-8 col-sm-7 col-xs-12',
          button: 'font-size: 14px; padding: 7px; margin-top: -6px;'
        },
        modalData: createModalData()
      }
    },
    methods: {
      getData: function () {
        var self = this
        this.$http.get(this.resource_url)
        .then(
          function (response) {
            self.graph = response.data.graph
          }).catch(function (error) {
            console.log(error)
            self.modalData = errors.connection
            self.$store.dispatch('openModal')
          })
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
      },
      performAction: function (action) {
        if (action === 'play-forceatlas') {
          this.s.startForceAtlas2({worker: true, barnesHutOptimize: false})
        } else if (action === 'pause-forceatlas') {
          this.s.stopForceAtlas2()
        }
      }
    },
    created: function () {
      this.getData()
    },
    watch: {
      graph: function (value) {
        if (this.graphHasData) {
          this.renderGraph()
        }
      }
    },
    computed: {
      graphHasData: function () {
        if (Object.keys(this.graph).includes('nodes')) {
          if (this.graph.nodes.length > 0) {
            return true
          }
        }
        return false
      }
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
  button {
    font-size: 15px;
  }
  .action-button {
    margin-left: 3px;
  }
  .tooltip-header {
    text-align: center;
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 2px
  }
  .tooltip-info {
    text-align: center;
    font-size: 12px;
    margin-bottom: 15px;
    padding-bottom: 5px;
    border-bottom: 1px solid #eee
  }
</style>
