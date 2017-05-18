<template>
  <div class="app-paginator">
    <button class="btn btn-default" v-on:click="fetchData(prev_page_url)" :disabled="!prev_page_url">
      {{config.previous_button_text}}
      <icon v-if="config.previous_button_text.length === 0" name="chevron-left"></icon>
    </button>
    <span>Page {{current_page}} of {{last_page}}</span>
    <button class="btn btn-default" v-on:click="fetchData(next_page_url)" :disabled="!next_page_url">
      {{config.next_button_text}}
      <icon v-if="config.next_button_text.length === 0" name="chevron-right"></icon>
    </button>
  </div>
</template>

<script>
  export default {
    props: {
      resource_url: {
        type: String,
        required: true
      },
      options: {
        type: Object,
        required: false,
        default () {
          return {}
        }
      }
    },
    data () {
      return {
        current_page: '',
        last_page: '',
        next_page_url: '',
        prev_page_url: '',
        config: {
          remote_data: 'data',
          remote_current_page: 'current_page',
          remote_last_page: 'last_page',
          remote_next_page_url: 'next_page_url',
          remote_prev_page_url: 'prev_page_url',
          previous_button_text: 'Previous',
          next_button_text: 'Next'
        }
      }
    },
    methods: {
      fetchData (pageUrl) {
        this.$emit('request-start')
        pageUrl = pageUrl || this.resource_url
        var self = this
        this.$http.get(pageUrl, { headers: this.config.headers })
        .then(function (response) {
          self.$emit('request-finish', response)
          self.handleResponseData(response.data)
        }).catch(function (response) {
          self.$emit('request-error', response)
          console.log('Fetching data failed.', response)
        })
      },
      handleResponseData (response) {
        this.makePagination(response)
        let data = this.getNestedValue(response, this.config.remote_data)
        this.$emit('update', data)
      },
      makePagination (data) {
        this.current_page = this.getNestedValue(data, this.config.remote_current_page)
        this.last_page = this.getNestedValue(data, this.config.remote_last_page)
        this.next_page_url = (this.current_page === this.last_page) ? null : this.getNestedValue(data, this.config.remote_next_page_url)
        this.prev_page_url = (this.current_page === 1) ? null : this.getNestedValue(data, this.config.remote_prev_page_url)
      },
      initConfig () {
        this.config = this.merge_objects(this.config, this.options)
      },
      merge_objects (obj1, obj2) {
        let obj3 = {}
        for (let attrname in obj1) { obj3[attrname] = obj1[attrname] }
        for (let attrname in obj2) { obj3[attrname] = obj2[attrname] }
        return obj3
      },
      getNestedValue (obj, path) {
        let originalPath = path
        path = path.split('.')
        let res = obj
        for (let i = 0; i < path.length; i++) {
          res = res[path[i]]
        }
        if (typeof res === 'undefined') {
          console.log(`Response doesn't contain key ${originalPath}!`)
        }
        return res
      }
    },
    watch: {
      resource_url () {
        this.fetchData()
      }
    },
    created () {
      this.initConfig()
      this.fetchData()
    }
  }
</script>

<style scoped>
  .fa-icon {
    width: auto;
    height: 1em;
    margin: 3px;
  }
  button {
    font-size: 15px;
    line-height: 1px;
  }
</style>
