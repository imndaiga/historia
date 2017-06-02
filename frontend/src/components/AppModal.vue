<template>
  <div v-if="modalIsOpen" class="modal-mask">
    <div class="modal-dialog">
      <div class="modal-content">
        <div v-if="headerIcon.length > 0 || header.length > 0 || type === 'alert'" class="modal-header" :style="{ 'background-color': headerColor}">
          <div class="row">
            <div class="col-xs-11" :style="{ color : headerTextColor }">
              <icon v-if="headerIcon.length > 0" :name="headerIcon"></icon>
              <span v-if="header.length > 0" class="modal-header-text">{{ header }}</span>
            </div>
            <a v-if="type === 'alert'" class="col-xs-1" v-on:click="closeModal" :style="{ color : headerTextColor }">&times;</a>
          </div>
        </div>
        <div class="modal-body">
          <slot name="form"></slot>
          <slot></slot>
        </div>
        <div v-if="type === 'form'" class="modal-footer">
          <button type="button" class="btn btn-danger" v-on:click="closeModal">Close</button>
          <button type="submit" v-on:click="submitForm" :class="['btn', 'btn-primary', {'disabled-button' : !modalIsActive}]">{{ submitMessage }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    props: {
      header: {
        required: false,
        type: String
      },
      headerIcon: {
        required: false,
        type: String
      },
      submitMessage: {
        required: false,
        type: String
      },
      color: {
        required: false,
        type: String
      },
      type: {
        required: false,
        type: String
      }
    },
    data: function () {
      return {
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
        this.$slots.form[0].componentInstance.submitForm()
      }
    },
    computed: {
      headerTextColor: function () {
        return this.color === '#fff' ? '#000' : '#fff'
      },
      headerColor: function () {
        return this.color === 'default' ? '#00c4a9' : this.color
      },
      ...mapState({
        modalIsOpen: 'modalIsOpen'
      })
    },
    created: function () {
      this.$on('form-field-activated', function () {
        this.modalIsActive = true
      }.bind(this))
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
