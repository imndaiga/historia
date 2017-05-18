<template>
  <div id="sigma-parent">
    <app-reload v-if="!graph_Is_Ready" message="No Relationship Data Available" v-on:reload-resource="forceReload"></app-reload>
    <div id="sigma-container" class="col-lg-12 col-md-12 col-sm-12 col-xs-12"></div>
  </div>
</template>

<script>
  import 'sigma/build/sigma.min.js'
  import 'sigma/plugins/sigma.layout.forceAtlas2/supervisor.js'
  import 'sigma/plugins/sigma.layout.forceAtlas2/worker.js'
  import AppReload from '@/components/AppReload'

  export default {
    components: {
      AppReload: AppReload
    },
    data: function () {
      return {
        graph: {},
        resource_url: '/api/graph',
        loading: false,
        s: { graph: '' }
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
  }
  .page-message {
    margin-top: 20%;
    font-size: 20px
  }
</style>
