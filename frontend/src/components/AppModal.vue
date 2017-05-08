<template>
  <div v-if="open_modal" class="modal-mask">
    <div class="modal-dialog">
      <div class="modal-content">
        <div v-if="title.length > 0 && header_icon.length > 0" class="modal-header">
          <icon :name="header_icon"></icon>
          <span class="modal-title">{{modal_title}}</span>
        </div>
        <div class="modal-body">
          <a v-if="title.length === 0 && header_icon.length === 0" v-on:click="closeModal">&times;</a>
          <component is=""></component>
        </div>
        <div v-if="submit_message.length > 0" class="modal-footer">
          <button type="button" class="btn btn-danger" v-on:click="closeModal">Close</button>
          <button type="submit" v-on:click="submitForm" :class="['btn', 'btn-primary']">{{submit_message}}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import bus from '../utils/bus'
  export default {
    data: function () {
      return {
        open_modal: false,
        title: '',
        header_icon: '',
        submit_message: ''
      }
    },
    methods: {
      closeModal: function () {
        document.getElementsByTagName('body')[0].classList.remove('stop-scrolling')
        this.open_modal = false
        this.title = ''
        this.header_icon = ''
        this.submit_message = ''
      },
      submitForm: function () {
        bus.$emit('submit-form')
      }
    },
    created: function () {
      bus.$on('open-modal', function (title, icon, submitMessage) {
        document.getElementsByTagName('body')[0].classList.add('stop-scrolling')
        this.open_modal = true
        this.modal_title = title || ''
        this.header_icon = icon || ''
        this.submit_message = submitMessage || ''
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
    max-height: calc(100vh - 250px);
    overflow-y: auto
  }

  .modal-body a {
    position: absolute;
    top: 10px;
    right: 20px;
    font-size: 25px;
    margin-left: 50px;
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
</style>
