<template>
  <div v-if="open_modal" class="modal-mask">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <i :class="modal_header_icon"></i>
          <span class="modal-title">{{modal_title}}</span>
        </div>
        <div class="modal-body">
          <hook-app-form ref="form" :form="modal_Form_Data" :submit_resource="submit_url" :search_resource="search_url" :form_is_inline="inlined_form"></hook-app-form>
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
    data: function () {
      return {
        raw_modal_form_data: [],
        open_modal: false,
        activate_submit_button: false,
        inlined_form: false,
        modal_title: '',
        modal_header_icon: '',
        modal_submit_message: '',
        submit_url: '',
        search_url: ''
      }
    },
    methods: {
      closeModal: function () {
        document.getElementsByTagName('body')[0].classList.remove('stop-scrolling')
        this.raw_modal_form_data = []
        this.open_modal = false
        this.activate_submit_button = false
        this.inlined_form = false
        this.modal_title = ''
        this.modal_header_icon = ''
        this.modal_submit_message = ''
        this.submit_url = ''
        this.search_url = ''
      },
      getModalFormData: function (URL, ID) {
        console.log('Retrieving form data')
      },
      submitForm: function () {
        this.$refs.form.submitForm()
      }
    },
    created: function () {
      this.$nuxt.$on('open-modal', function (form, getFormUrl, recordId, modalTitle) {
        document.getElementsByTagName('body')[0].classList.add('stop-scrolling')
        if (!form) {
          this.modal_title = modalTitle
          this.getModalFormData(getFormUrl, recordId)
        } else {
          this.raw_modal_form_data = form.data
          this.activate_submit_button = true
          this.inlined_form = false
          this.modal_title = form.modal_title
          this.modal_header_icon = form.modal_icon
          this.modal_submit_message = form.modal_submit_message
          this.submit_url = form.resource_urls.submit_url
          this.search_url = form.resource_urls.search_url
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
    margin-top: 80px;
    overflow-y: initial !important
  }

  .modal-body {
    max-height: calc(100vh - 180px);
    overflow-y: auto
  }

  .modal-mask {
    position: fixed;
    z-index: 1001;
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
