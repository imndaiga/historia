<template>
  <div id="sigma-parent">
    <p v-if="!graph_Is_Ready" class="page-message text-center">No Relationship Data Available</p>
    <div id="sigma-container" class="col-lg-12 col-md-12 col-sm-12 col-xs-12"></div>
  </div>
</template>

<script>
  import Sigma from 'sigma'
  export default {
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
            self.loading = false
          }).catch(function (error) {
            console.log(error)
            self.loading = false
          })
      },
      renderGraph: function () {
        this.s = new Sigma({
          graph: this.graph,
          container: 'sigma-container',
          settings: {
            defaultLabelSize: 20,
            font: 'Open Sans',
            labelThreshold: 12
          }
        })
        this.s.refresh()
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
