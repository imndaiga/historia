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
              <td v-for="(value, key) in record" v-if="key !== 'id'" :key="record.id">{{ value }}</td>
              <td class="center-content">
                <app-tooltip v-on:perform-action="performAction" :anchorKey="record.id" icon="ellipsis-h" position="left" arrowSize="small" anchorClass="hidden-lg hidden-md">
                  <div slot="template" class="hidden-xs hidden-sm">
                    <button type="button" v-for="button in rowActions" v-on:click="performAction(button.action, record.id, getFullName([record.first_name, record.ethnic_name, record.last_name]), button.url)" :class="button.class" :title="button.title" :action="[button.action, button.url, getFullName([record.first_name, record.ethnic_name, record.last_name]), record.id]">
                      <icon :name="button.icon"></icon>
                    </button>
                  </div>
                </app-tooltip>
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
    <app-modal :header="modalData.header" :headerIcon="modalData.headerIcon" :submitMessage="modalData.submitMessage" :color="modalData.color" :type="modalData.type" :modalIsOpen="modalData.open">
      <child-form slot="form" v-if="modalData.type === 'form'" :rawForm="rawForm" :submitUrl="modalData.submitUrl" :searchUrl="modalData.searchUrl"></child-form>
      <div v-else-if="modalData.type === 'alert'">
        <p class="alert-header">{{ modalData.subject }}</p>
        <p class="alert-message" v-if="modalData.message.length > 0">{{ modalData.message }}</p>
      </div>
    </app-modal>
  </div>
</template>

<script>
  import AppPaginator from './AppPaginator.vue'
  import AppReload from './AppReload.vue'
  import AppTooltip from './AppTooltip'
  import { createModalData, errors } from '@/utils/helper'
  import AppModal from './AppModal.vue'
  import ChildForm from './ChildForm.vue'

  export default {
    components: {
      AppPaginator: AppPaginator,
      AppReload: AppReload,
      AppTooltip: AppTooltip,
      AppModal: AppModal,
      ChildForm: ChildForm
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
        rowActions: [
          {
            url: '/api/person',
            title: 'Edit',
            action: 'edit-record',
            class: 'btn btn-sm btn-default action-button',
            icon: 'user',
            submitUrl: '/api/person',
            searchUrl: ''
          },
          {
            url: '/api/person/family',
            title: 'Edit',
            action: 'edit-record',
            class: 'btn btn-sm btn-default action-button',
            icon: 'link',
            submitUrl: '/api/relationships',
            searchUrl: '/api/person'
          },
          {
            url: '',
            title: 'Delete',
            action: 'delete-record',
            class: 'btn btn-sm btn-danger action-button',
            icon: 'trash-o'
          }
        ],
        modalData: createModalData(),
        rawForm: []
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
        this.modalData = errors.connection
        this.$store.dispatch('openModal')
      },
      performAction: function (action, personId, fullName, resourceUrl) {
        if (action === 'edit-record') {
          for (let index in this.rowActions) {
            if (this.rowActions[index].url === resourceUrl) {
              var submitUrl = this.rowActions[index].submitUrl
              var searchUrl = this.rowActions[index].searchUrl
            }
          }
          this.openRecord(personId, fullName, resourceUrl, submitUrl, searchUrl)
        } else if (action === 'delete-record') {
          this.deleteRecord(personId)
        }
      },
      openRecord: function (personId, fullName, resourceUrl, submitUrl, searchUrl) {
        var self = this
        this.$http.get(resourceUrl, {
          params: {
            id: personId
          }
        })
        .then(function (response) {
          self.rawForm = response.data
          self.modalData = createModalData('edit', fullName, null, null, null, 'form', 'Save Changes', submitUrl, searchUrl)
          self.$store.dispatch('openModal')
        }).catch(function (error) {
          console.log(error)
          self.modalData = errors.action
          self.$store.dispatch('openModal')
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
          var pageNumber = self.$refs.paginator.current_page
          var reloadUrl = self.resource_url + '?page=' + pageNumber
          self.$refs.paginator.fetchData(reloadUrl)
        }).catch(function (error) {
          console.log(error)
          self.modalData = errors.action
          self.$store.dispatch('openModal')
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
        for (let record in this.raw_table_data) {
          let fieldName = ''
          let fieldValue = ''
          for (let field in this.raw_table_data[record]) {
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
      margin: 20% 0 0 0;
    }
  }

  @media (min-width: 992px) {
    .app-table {
      margin: 8% 0 0 0;
    }
  }
</style>
