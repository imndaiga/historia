<template>
  <div class="app-table">
    <div v-if="table_Data.length > 0">
      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th class="center-content" v-for="header in table_Headers">{{header}}</th>
              <th class="center-content">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in table_Data">
              <td class="center-content" v-for="(value, key) in record" v-if="key !== 'id'">{{ value }}</td>
              <td class="center-content">
                <button type="button" v-on:click="openRecord(record.id, [record.first_name, record.ethnic_name, record.last_name], '/api/person')" class="btn btn-default btn-sm" title="Edit">
                  <icon name="user"></icon>
                </button>
                <button type="button" v-on:click="openRecord(record.id,  [record.first_name, record.ethnic_name, record.last_name], 'api/person/family')" class="btn btn-default btn-sm" title="Edit">
                  <icon name="link"></icon>
                </button>
                <button type="button" class="btn btn-danger btn-sm" v-on:click="deleteRecord(record.id)" title="Delete">
                  <icon name="trash-o"></icon>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <app-reload v-else message="No Relationship Data Available" v-on:reload-resource="forceReload"></app-reload>
    <div class="row" v-show="table_Data.length > 0">
      <app-paginator class="col-lg-3 col-lg-push-5 col-md-4 col-md-push-4 col-sm-5 col-sm-push-4 col-xs-6 col-xs-push-4" :resource_url="resource_url" v-on:update="updateTable" v-on:request-error="paginateLoadError" :options="options" ref="paginator"></app-paginator>
    </div>
  </div>
</template>

<script>
  import AppPaginator from './AppPaginator.vue'
  import AppReload from './AppReload.vue'
  import bus from '@/utils/bus'

  export default {
    components: {
      AppPaginator: AppPaginator,
      AppReload: AppReload
    },
    props: {
      resource_url: {
        type: String,
        required: true
      }
    },
    data: function () {
      return {
        raw_table_data: [],
        options: {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('id_token')
          },
          next_button_text: '',
          previous_button_text: ''
        }
      }
    },
    methods: {
      updateTable: function (data) {
        this.raw_table_data = data
      },
      forceReload: function (data) {
        this.$refs.paginator.fetchData()
      },
      paginateLoadError: function () {
        bus.$emit('modal-data-ready', 'Ooops!', 'exclamation-circle', null, null, 'An error occured!', 'Something went wrong while retrieving data.', 'red')
      },
      openRecord: function (personId, nameList, resourceUrl) {
        var fullName = nameList.filter(function (val) { return val }).join(' ')
        this.$http.get(resourceUrl, {
          params: {
            id: personId
          }
        })
        .then(function (response) {
          var form = response.data
          bus.$emit('modal-data-ready', fullName, 'edit', form, 'Save Changes', null)
        }).catch(function (error) {
          console.log(error)
          bus.$emit('modal-data-ready', 'Ooops!', 'exclamation-circle', null, null, 'An error occured!', 'Something went wrong while performing action.', 'red')
        })
      },
      deleteRecord: function (recordId) {
        var self = this
        this.$http.delete(this.resource_url, {
          data: {
            id: recordId
          }
        })
        .then(function (response) {
          for (var record in self.raw_table_data) {
            for (var field in self.raw_table_data[record]) {
              if (self.raw_table_data[record][field].field_name === 'id') {
                if (self.raw_table_data[record][field].value === recordId) {
                  self.raw_table_data.splice(record, 1)
                }
              }
            }
          }
        }).catch(function (error) {
          console.log(error)
          bus.$emit('modal-data-ready', 'Ooops!', 'exclamation-circle', null, null, 'An error occured!', 'Something went wrong while performing action.', 'red')
        })
      }
    },
    computed: {
      table_Headers: function () {
        var headers = []
        for (var record in this.raw_table_data) {
          for (var field in this.raw_table_data[record]) {
            var header = this.raw_table_data[record][field].label
            if (headers.indexOf(header) === -1 && header !== 'ID') {
              headers.push(this.raw_table_data[record][field].label)
            }
          }
        }
        return headers
      },
      table_Data: function () {
        var records = []
        var entry = {}
        for (var record in this.raw_table_data) {
          var fieldName = ''
          var fieldValue = ''
          for (var field in this.raw_table_data[record]) {
            fieldName = this.raw_table_data[record][field].field_name
            fieldValue = this.raw_table_data[record][field].value
            entry[fieldName] = fieldValue
          }
          records.push(entry)
          entry = {}
        }
        return records
      }
    }
  }
</script>

<style scoped>
  .fa-icon {
    width: auto;
    height: 1em;
  }

  button {
    font-size: 15px;
  }

  .app-table {
    margin: 2%;
  }

  .center-content {
    text-align: center
  }
</style>
