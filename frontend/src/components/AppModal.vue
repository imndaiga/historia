<template>
  <div v-if="modalData" class="modal-mask">
    <div class="modal-dialog">
      <div class="modal-content">
        <div v-if="modalData.header_icon.length > 0 || modalData.header.length > 0 || modalType === 'alert'" class="modal-header" :style="{ 'background-color': headerColor}">
          <div class="row">
            <div class="col-xs-11" :style="{ color : headerTextColor }">
              <icon v-if="modalData.header_icon.length > 0" :name="modalData.header_icon"></icon>
              <span v-if="modalData.header.length > 0" class="modal-header-text">{{ modalData.header }}</span>
            </div>
            <a v-if="modalType === 'alert'" class="col-xs-1" v-on:click="closeModal" :style="{ color : headerTextColor }">&times;</a>
          </div>
        </div>
        <div class="modal-body">
          <child-form v-if="modalType === 'form'" :raw_form="modalData.form" submit_url="/submit" search_url="/search" ref="form"></child-form>
          <div v-else-if="modalType === 'alert'">
            <p class="alert-header">{{ modalData.subject }}</p>
            <p class="alert-message" v-if="modalData.message.length > 0">{{ modalData.message }}</p>
          </div>
        </div>
        <div v-if="modalType === 'form'" class="modal-footer">
          <button type="button" class="btn btn-danger" v-on:click="closeModal">Close</button>
          <button type="submit" v-on:click="submitForm" :class="['btn', 'btn-primary', {'disabled-button' : !modalIsActive}]">{{ modalData.button_submit_message }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import ChildForm from './ChildForm'
  import bus from '@/utils/bus'
  import { mapState } from 'vuex'

  export default {
    components: {
      ChildForm: ChildForm
    },
    data: function () {
      return {
        modalType: null,
        modalIsActive: false
      }
    },
    methods: {
      closeModal: function () {
        document.getElementsByTagName('body')[0].classList.remove('stop-scrolling')
        this.modalIsActive = false
        this.$store.dispatch('closeModal')
      },
      submitForm: function () {
        this.$refs.form.submitForm()
      }
    },
    created: function () {
      bus.$on('form-field-activated', function () {
        this.modalIsActive = true
      }.bind(this))
    },
    computed: {
      headerTextColor: function () {
        return this.modalData.color === '#fff' ? '#000' : '#fff'
      },
      headerColor: function () {
        return this.modalData.color === 'default' ? '#00c4a9' : this.modalData.color
      },
      modalData: function () {
        if (this.form.open) {
          this.modalType = 'form'
          return this.form
        } else if (this.alert.open) {
          this.modalType = 'alert'
          return this.alert
        } else {
          this.modalType = null
          return null
        }
      },
      ...mapState({
        form: 'modal_form',
        alert: 'modal_alert'
      })
    }
  }
</script>

<style scoped>
  .fa-icon {
    vertical-align: -17%
  }

  .modal-content {
    border-radius: 0px;
  }

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

  .modal-header-text {
    font-size: 20px;
    font-weight: 400;
    padding-left: 10px
  }

  .disabled-button {
    display: none
  }

  .alert-header {
    font-size: 20px;
    font-weight: 600;
    text-align: center;
  }

  .alert-message {
    font-size: 15px;
    font-weight: 400;
    text-align: center;
  }
</style>
