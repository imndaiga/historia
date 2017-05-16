<template>
  <div v-if="open_modal" class="modal-mask">
    <div class="modal-dialog">
      <div class="modal-content">
        <div v-if="header_icon.length > 0 || title.length > 0 || submit_message.length === 0" class="modal-header">
          <div class="row">
            <div class="col-xs-11">
              <icon v-if="header_icon.length > 0" :name="header_icon"></icon>
              <span v-if="title.length > 0" class="modal-title">{{title}}</span>
            </div>
            <a v-if="submit_message.length === 0" class="col-xs-1" v-on:click="closeModal">&times;</a>
          </div>
        </div>
        <div class="modal-body">
          <child-form v-if="form.length > 0" :raw_form="form" submit_url="/submit" search_url="/search"></child-form>
          <p class="alert-message" v-else-if="alert.length > 0">{{alert}}</p>
        </div>
        <div v-if="submit_message.length > 0" class="modal-footer">
          <button type="button" class="btn btn-danger" v-on:click="closeModal">Close</button>
          <button type="submit" v-on:click="submitForm" :class="['btn', 'btn-primary', {'disabled-button' : !modal_is_active}]">{{submit_message}}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import ChildForm from './ChildForm'
  import bus from '../utils/bus'

  export default {
    components: {
      ChildForm: ChildForm
    },
    data: function () {
      return {
        open_modal: false,
        title: '',
        header_icon: '',
        submit_message: '',
        modal_is_active: false,
        alert: '',
        form: []
      }
    },
    methods: {
      closeModal: function () {
        document.getElementsByTagName('body')[0].classList.remove('stop-scrolling')
        this.open_modal = false
        this.title = ''
        this.header_icon = ''
        this.submit_message = ''
        this.modal_is_active = false
      },
      submitForm: function () {
        bus.$emit('submit-form')
      }
    },
    created: function () {
      bus.$on('modal-data-ready', function (title, icon, form, submitMessage, alert) {
        document.getElementsByTagName('body')[0].classList.add('stop-scrolling')
        this.open_modal = true
        this.title = title || ''
        this.form = form || []
        this.header_icon = icon || ''
        this.submit_message = submitMessage || ''
        this.alert = alert || ''
      }.bind(this))
      bus.$on('form-field-activated', function () {
        this.modal_is_active = true
      }.bind(this))
    }
  }
</script>

<style scoped>
  .modal-dialog {
    margin-top: 80px;
    overflow-y: initial !important
  }

  .modal-body {
    min-height: 100px;
    max-height: calc(100vh - 260px);
    overflow-y: auto
  }

  .modal-header {
    font-size: 25px;
  }
  .modal-header a {
    text-decoration: none;
    cursor: pointer;
    color: black;
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

  .disabled-button {
    display: none
  }

  .alert-message {
    font-size: 40px;
    font-weight: 600;
    text-align: center;
  }
</style>
