<template>
  <div v-if="open_modal" class="modal-mask">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <i :class="modal_header_icon"></i>
          <span class="modal-title">{{modal_title}}</span>
        </div>
        <div class="modal-body">
          <hook-app-form :form="modal_Form_Data" :submit_resource="resource_urls.submit_resource" :search_resource="resource_urls.search_resource" :form_is_inline="inlined_form"></hook-app-form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-danger" v-on:click="closeModal">Close</button>
          <button type="submit" v-on:click="submitForm" :class="['btn', 'btn-primary', {'disabled-button' : !activate_submit_button}]">{{modal_submit_message}}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import HookAppForm from '~components/HookAppForm.vue'
  import { required, email, alpha } from 'vuelidate/lib/validators'
  function extendDict (obj, src) {
    for (var key in src) {
      if (src.hasOwnProperty(key)) {
        obj[key] = src[key]
      }
      return obj
    }
  }
  export default {
    components: {
      HookAppForm: HookAppForm
    },
    props: {
      resource_urls: {
        type: Object,
        required: true
      }
    },
    data: function () {
      return {
        open_modal: false,
        raw_modal_form_data: [],
        activate_submit_button: false,
        resource_url: '',
        inlined_form: false,
        modal_title: '',
        modal_header_icon: 'fa fa-pencil-square-o fa-lg',
        modal_submit_message: ''
      }
    },
    methods: {
      closeModal: function () {
        self.raw_modal_form_data = []
        this.open_modal = false
        this.activate_submit_button = false
        this.modal_title = ''
        document.getElementsByTagName('body')[0].classList.remove('stop-scrolling')
      },
      getModalFormData: function (recordId) {
        console.log('Retrieving form data')
      },
      submitForm: function () {
        console.log('Submitting form')
      }
    },
    created: function () {
      this.$nuxt.$on('open-modal', function (form, resource, recordId, title) {
        if (!form) {
          for (var url in this.resource_urls) {
            if (url === resource) {
              this.resource_url = this.resource_urls[url]
            }
          }
          document.getElementsByTagName('body')[0].classList.add('stop-scrolling')
          this.modal_title = title
          this.getModalFormData(recordId)
        } else {
          this.raw_modal_form_data = form
          this.inlined_form = false
          this.modal_header_icon = ''
          this.modal_title = 'Login'
          this.activate_submit_button = true
          this.modal_header_icon = 'fa fa-sign-in fa-lg'
          this.modal_submit_message = 'Log In'
          this.open_modal = true
        }
      }.bind(this))
      this.$nuxt.$on('form-field-activated', function () {
        this.activate_submit_button = true
      }.bind(this))
    },
    computed: {
      modal_Form_Data: function () {
        var processed = this.raw_modal_form_data
        for (var field in this.raw_modal_form_data) {
          if (this.raw_modal_form_data[field].validators !== undefined) {
            var fieldValidators = this.raw_modal_form_data[field].validators
            processed[field].validators = {}
            for (var index in fieldValidators) {
              if (fieldValidators[index] === 'required') {
                processed[field].validators = extendDict(processed[field].validators, {required})
              } else if (fieldValidators[index] === 'alpha') {
                processed[field].validators = extendDict(processed[field].validators, {alpha})
              } else if (fieldValidators[index] === 'email') {
                processed[field].validators = extendDict(processed[field].validators, {email})
              }
            }
          }
        }
        return processed
      }
    }
  }
</script>

<style scoped>
  .modal-dialog {
    overflow-y: initial !important
  }

  .modal-body {
    max-height: calc(100vh - 180px);
    overflow-y: auto
  }

  .modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, .5);
    display: table
  }

  .modal-title {
    font-size: 20px;
    font-weight: 600;
    padding-left: 10px
  }
</style>
