<template>
  <div class="col-lg-10 col-lg-push-2 col-md-9 col-md-push-3 col-sm-8 col-sm-push-4 col-xs-12">
    <page-header></page-header>
    <div class="panel-group">
      <div v-for="panel in panels" class="col-lg-6 col-md-6 col-sm-6">
        <base-panel :panel="panel" :key="panel.key">
          <hook-app-form :form="panel.form" :submit_resource="panel.submit_resource" :search_resource="panel.search_resource" :form_is_inline="false"></hook-app-form>
        </base-panel>
      </div>
    </div>
  </div>
</template>

<script>
  import PageHeader from '~components/PageHeader.vue'
  import BasePanel from '~components/BasePanel.vue'
  import HookAppForm from '~components/HookAppForm.vue'
  import { required, email, alpha } from 'vuelidate/lib/validators'
  export default {
    fetch: function ({ store, redirect }) {
      if (!store.state.authUser) {
        return redirect('/')
      }
    },
    layout: 'dashboard',
    components: {
      PageHeader: PageHeader,
      BasePanel: BasePanel,
      HookAppForm: HookAppForm
    },
    data: function () {
      return {
        panels: [
          {
            name: 'add_relative_panel',
            open: false,
            label: 'Add Relative',
            icon: 'fa fa-user-plus fa-fw',
            submit_resource: '',
            search_resource: '',
            form: [
              {
                type: 'alpha-input',
                placeholder: 'Enter First Name',
                label: 'First Name',
                validators: { required, alpha },
                field_name: 'first_name',
                classes: '',
                key: 1
              },
              {
                type: 'alpha-input',
                placeholder: 'Enter Ethnic Name',
                label: 'Ethnic Name',
                validators: { required, alpha },
                field_name: 'ethnic_name',
                classes: '',
                key: 2
              },
              {
                type: 'alpha-input',
                placeholder: 'Enter Last Name',
                label: 'Last Name',
                validators: { required, alpha },
                field_name: 'last_name',
                classes: '',
                key: 3
              },
              {
                type: 'email-input',
                placeholder: 'Enter Email Address',
                label: 'Email',
                validators: { email },
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
              },
              {
                type: 'submit-button',
                button_message: 'Save Relative',
                button_name: 'add_personal-details',
                button_class: 'btn btn-lg btn-success btn-block btn-margin',
                key: 9
              }
            ],
            key: 1
          },
          {
            name: 'add_relationship_panel',
            open: false,
            label: 'Add Relationship',
            icon: 'fa fa-link fa-fw',
            submit_resource: '',
            search_resource: '',
            form: [
              {
                type: 'search-input',
                placeholder: 'Search for Relative',
                label: 'From',
                validators: { required },
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
                validators: { required },
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
                validators: { required },
                field_name: 'relation_name',
                classes: '',
                multiselect_options: ['Parent', 'Partner', 'Sibling', 'Step-Parent', 'Step-Sibling', 'Child'],
                SelectLabel: '',
                DeselectLabel: '',
                key: 7
              },
              {
                type: 'submit-button',
                button_message: 'Save Relationship',
                button_name: 'add_connect-relations',
                bs_panel: 'add_relationship_panel',
                button_class: 'btn btn-lg btn-success btn-block btn-margin',
                key: 10
              }
            ],
            key: 2
          }
        ]
      }
    }
  }
</script>

<style scoped>
  .panel-group {
    margin: 20px
  }
</style>
