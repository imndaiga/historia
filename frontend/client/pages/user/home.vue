<template>
  <div class="col-lg-10 col-lg-push-2 col-md-9 col-md-push-3 col-sm-8 col-sm-push-4 col-xs-12">
    <page-header></page-header>
    <actions-bar :title="actions_bar_title" :buttons="[actions_data[0].button, actions_data[1].button]"></actions-bar>
    <base-modal-form></base-modal-form>
  </div>
</template>

<script>
  import PageHeader from '~components/PageHeader.vue'
  import ActionsBar from '~components/ActionsBar.vue'
  import BaseModalForm from '~components/BaseModalForm.vue'
  export default {
    middleware: 'authenticated',
    layout: 'dashboard',
    components: {
      PageHeader: PageHeader,
      ActionsBar: ActionsBar,
      BaseModalForm: BaseModalForm
    },
    data: function () {
      return {
        actions_bar_title: 'Quick Actions',
        actions_data: [
          {
            button: {
              message: 'Add Relative',
              icon: 'fa fa-user-plus fa-fw',
              action: 'open_add_relative_modal'
            },
            form: {
              data: [
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
              ],
              modal_title: 'Add Relative',
              modal_icon: 'fa fa-user-plus fa-fw',
              modal_submit_message: 'Add Relative',
              inline: false,
              resource_urls: {
                submit_url: 'api/person',
                search_url: ''
              }
            },
            key: 1
          },
          {
            button: {
              message: 'Add Relationship',
              icon: 'fa fa-link fa-fw',
              action: 'open_add_relation_modal'
            },
            form: {
              data: [
                {
                  type: 'search-input',
                  placeholder: 'Search for Relative',
                  label: 'From',
                  validators: ['required'],
                  field_name: 'from_person',
                  classes: '',
                  SelectLabel: '',
                  DeselectLabel: '',
                  key: 5
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
                  key: 6
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
                  key: 7
                }
              ],
              modal_title: 'Add Relationship',
              modal_icon: 'fa fa-link fa-fw',
              modal_submit_message: 'Add Relationship',
              inline: false,
              resource_urls: {
                submit_url: 'api/relationships',
                search_url: ''
              }
            },
            key: 2
          }
        ]
      }
    },
    created: function () {
      this.$nuxt.$on('open_add_relative_modal', function () {
        this.$nuxt.$emit('open-modal', JSON.stringify(this.actions_data[0].form))
      }.bind(this))
      this.$nuxt.$on('open_add_relation_modal', function () {
        this.$nuxt.$emit('open-modal', JSON.stringify(this.actions_data[1].form))
      }.bind(this))
    }
  }
</script>

<style scoped>
  .panel-group {
    margin: 20px
  }
</style>
