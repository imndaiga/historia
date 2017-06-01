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
              <td v-for="(value, key) in record" v-if="key !== 'id'">{{ value }}</td>
              <td class="center-content">
                <div :ref="'tooltip-template-' + record.id" class="hidden-xs hidden-sm" v-tooltip="{ key: record.id, icon: 'ellipsis-h', position: 'left', arrow_size: 'small' }">
                  <button type="button" v-for="button in row_actions" v-on:click="performAction(button.action, record.id, getFullName([record.first_name, record.ethnic_name, record.last_name]), button.url)" :class="button.class" :title="button.title" :action="[button.action, button.url, getFullName([record.first_name, record.ethnic_name, record.last_name]), record.id]">
                    <icon :name="button.icon"></icon>
                  </button>
                </div>
                <app-tooltip class="hidden-md hidden-lg"></app-tooltip>
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
  import AppTooltip from './AppTooltip'
  import bus from '@/utils/bus'

  export default {
    components: {
      AppPaginator: AppPaginator,
      AppReload: AppReload,
      AppTooltip: AppTooltip
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
        },
        row_actions: [
          {
            url: '/api/person',
            title: 'Edit',
            action: 'edit-record',
            class: 'btn btn-sm btn-default action-button',
            icon: 'user'
          },
          {
            url: '/api/person/family',
            title: 'Edit',
            action: 'edit-record',
            class: 'btn btn-sm btn-default action-button',
            icon: 'link'
          },
          {
            url: '',
            title: 'Delete',
            action: 'delete-record',
            class: 'btn btn-sm btn-danger action-button',
            icon: 'trash-o'
          }
        ]
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
        var modal = {
          header: 'Ooops!',
          header_icon: 'exclamation-circle',
          subject: 'An error occured!',
          message: 'Something went wrong while retrieving data.',
          color: 'red',
          type: 'alert'
        }
        self.$store.dispatch('openModal', modal)
      },
      performAction: function (action, personId, fullName, resourceUrl) {
        if (action === 'edit-record') {
          this.openRecord(personId, fullName, resourceUrl)
        } else if (action === 'delete-record') {
          this.deleteRecord(personId)
        }
      },
      openRecord: function (personId, fullName, resourceUrl) {
        var self = this
        this.$http.get(resourceUrl, {
          params: {
            id: personId
          }
        })
        .then(function (response) {
          var form = response.data
          var modal = {
            header: fullName,
            header_icon: 'edit',
            button_submit_message: 'Save Changes',
            form: form,
            color: 'default',
            type: 'form'
          }
          self.$store.dispatch('openModal', modal)
        }).catch(function (error) {
          console.log(error)
          var modal = {
            header: 'Ooops!',
            header_icon: 'exclamation-circle',
            subject: 'An error occured!',
            message: 'Something went wrong while performing action.',
            color: 'red',
            type: 'alert'
          }
          self.$store.dispatch('openModal', modal)
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
          var modal = {
            header: 'Ooops!',
            header_icon: 'exclamation-circle',
            subject: 'An error occured!',
            message: 'Something went wrong while performing action.',
            color: 'red',
            type: 'alert'
          }
          self.$store.dispatch('openModal', modal)
        })
      },
      getFullName: function (nameList) {
        return nameList.filter(function (val) { return val }).join(' ')
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
    },
    created: function () {
      bus.$on('edit-record', function (personId, fullName, resourceUrl) {
        this.openRecord(personId, fullName, resourceUrl)
      }.bind(this))
      bus.$on('delete-record', function (personId) {
        this.deleteRecord(personId)
      }.bind(this))
    }
  }
</script>

<style scoped>
  button {
    font-size: 15px;
  }

  .app-table {
    margin: 2%;
  }

  .center-content {
    text-align: center
  }

  .action-button {
    margin-left: 3px;
  }

  @media (min-width: 768px) and (max-width: 992px) {
    .app-table {
      margin: 13% 0 0 0;
    }
  }
</style>
