<template>
  <div>
    <actions-bar :title="actions_bar_title"  :buttons="action_buttons" :styles="actions_bar_style" v-on:open-modal="openModal"></actions-bar>
    <card :header="'Welcome ' + user.nickname + '!'" headerIcon="user">
      <ul class="list-group">
        <li class="list-group-item list-group-item-success">
          <span>You have {{ userNodeSize }} members in your history tree!</span>
        </li>
      </ul>

    </card>
    <card bodyPadding="0px">
      <div class="add-panel" v-on:click="AddPanel">
        <icon name="plus"></icon>
      </div>
    </card>
    <app-modal :header="modalData.header" :headerIcon="modalData.headerIcon" :submitMessage="modalData.submitMessage" :color="modalData.color" :type="modalData.type" :modalIsOpen="modalData.open">
      <child-form slot="form" v-if="modalData.type === 'form'" :rawForm="selectedForm" :submitUrl="modalData.submitUrl" :searchUrl="modalData.searchUrl"></child-form>
      <div v-else-if="modalData.type === 'alert'">
        <p class="alert-header">{{ modalData.subject }}</p>
        <p class="alert-message" v-if="modalData.message.length > 0">{{ modalData.message }}</p>
      </div>
    </app-modal>
  </div>
</template>

<script>
  import AppActionsBar from '@/components/AppActionsBar.vue'
  import AppCard from '@/components/AppCard.vue'
  import AppModal from '@/components/AppModal.vue'
  import ChildForm from '@/components/ChildForm.vue'
  import { createModalData, errors } from '@/utils/helper'

  export default {
    components: {
      ActionsBar: AppActionsBar,
      Card: AppCard,
      AppModal: AppModal,
      ChildForm: ChildForm
    },
    data: function () {
      return {
        actions_bar_title: 'Quick Actions',
        action_buttons: [
          {
            message: 'Add Relative',
            icon: 'user-plus',
            action: 'open-modal',
            target: 'relative_form',
            key: 1
          },
          {
            message: 'Add Relationship',
            icon: 'link',
            action: 'open-modal',
            target: 'relationship_form',
            key: 2
          }
        ],
        actions_bar_style: {
          well: 'margin: 20px; background-color: #fff; border-radius: 0px',
          row: 'line-height: 45px; height: 45px',
          titleDivClass: 'col-lg-2 col-md-3 col-sm-5 hidden-xs',
          title: 'font-weight: 600; margin-left: 10px; font-size: 19px',
          buttonDivClass: 'col-lg-10 col-md-9 col-sm-7 col-xs-12',
          button: 'font-size: 17px;'
        },
        forms: {
          relationship_form: [
            {
              type: 'search-input',
              placeholder: 'Search for Relative',
              label: 'From',
              validators: ['required'],
              field_name: 'from_person',
              classes: '',
              SelectLabel: '',
              DeselectLabel: '',
              key: 1
            },
            {
              type: 'search-input',
              placeholder: 'Search for Relative',
              label: 'To',
              validators: ['required'],
              field_name: 'to_person',
              classes: '',
              SelectLabel: '',
              DeselectLabel: '',
              key: 2
            },
            {
              type: 'multiselect-input',
              placeholder: 'Choose a Relation',
              label: 'Relation',
              validators: ['required'],
              field_name: 'relation_name',
              classes: '',
              multiselect_options: ['Parent', 'Partner', 'Sibling', 'Step-Parent', 'Step-Sibling', 'Child'],
              SelectLabel: '',
              DeselectLabel: '',
              key: 3
            }
          ],
          relative_form: [
            {
              type: 'alpha-input',
              placeholder: 'Enter First Name',
              label: 'First Name',
              validators: ['required', 'alpha'],
              field_name: 'first_name',
              classes: '',
              key: 1
            },
            {
              type: 'alpha-input',
              placeholder: 'Enter Ethnic Name',
              label: 'Ethnic Name',
              validators: ['required', 'alpha'],
              field_name: 'ethnic_name',
              classes: '',
              key: 2
            },
            {
              type: 'alpha-input',
              placeholder: 'Enter Last Name',
              label: 'Last Name',
              validators: ['required', 'alpha'],
              field_name: 'last_name',
              classes: '',
              key: 3
            },
            {
              type: 'email-input',
              placeholder: 'Enter Email Address',
              label: 'Email',
              validators: ['email'],
              field_name: 'email',
              classes: '',
              key: 4
            },
            {
              type: 'pikaday-input',
              placeholder: 'Select Birth Date',
              label: 'Date of Birth',
              field_name: 'birth_date',
              classes: '',
              key: 8
            }
          ]
        },
        resourceUrls: {
          relative_form: {
            submitUrl: 'api/person',
            searchUrl: ''
          },
          relationship_form: {
            submitUrl: 'api/relationships',
            searchUrl: 'api/person'
          }
        },
        user: JSON.parse(localStorage.getItem('profile')),
        userNodeSize: {},
        selectedForm: [],
        modalData: createModalData()
      }
    },
    created: function () {
      this.getData()
    },
    methods: {
      AddPanel: function () {
        this.modalData = errors.development
        this.$store.dispatch('openModal')
      },
      getData: function () {
        var self = this
        this.$http.get('api/user/statistics')
        .then(function (response) {
          self.userNodeSize = response.data.nodeSize
        }).catch(function (error) {
          console.log(error)
          this.modalData = errors.connection
          this.$store.dispatch('openModal')
        })
      },
      openModal: function (targetForm) {
        for (var index in this.action_buttons) {
          if (this.action_buttons[index].target === targetForm) {
            var icon = this.action_buttons[index].icon
            var header = this.action_buttons[index].message
          }
        }
        this.selectedForm = this.forms[targetForm]
        var submitUrl = this.resourceUrls[targetForm].submitUrl
        var searchUrl = this.resourceUrls[targetForm].searchUrl
        this.modalData = createModalData(icon, header, null, null, null, 'form', 'Save', submitUrl, searchUrl)
        this.$store.dispatch('openModal')
      }
    }
  }
</script>

<style scoped>
  .add-panel {
    font-size: 60px;
    text-align: center;
    color: lightgrey;
    cursor: pointer;
    min-height: 120px;
    padding-top: 7%
  }
  .add-panel:focus,
  .add-panel:hover {
    color: grey;
    background-color: #f5f5f5;
  }
</style>
