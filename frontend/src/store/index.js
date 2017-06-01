import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    modal_form: {
      header: '',
      header_icon: '',
      button_submit_message: '',
      form: [],
      color: 'default',
      open: false
    },
    modal_alert: {
      header: '',
      header_icon: '',
      subject: '',
      message: '',
      color: 'default',
      open: false
    }
  },
  mutations: {
    triggerModalForm: function (state, modalForm) {
      state.modal_form.header = modalForm.header
      state.modal_form.header_icon = modalForm.header_icon
      state.modal_form.button_submit_message = modalForm.button_submit_message
      state.modal_form.form = modalForm.form
      state.modal_form.color = modalForm.color || 'default'
      state.modal_form.open = true
    },
    triggerModalAlert: function (state, modalAlert) {
      state.modal_alert.header = modalAlert.header
      state.modal_alert.header_icon = modalAlert.header_icon
      state.modal_alert.subject = modalAlert.subject
      state.modal_alert.message = modalAlert.message
      state.modal_alert.color = modalAlert.color || 'default'
      state.modal_alert.open = true
    },
    clearModalObjects: function (state) {
      state.modal_form = {
        header: '',
        header_icon: '',
        form: [],
        color: 'default',
        open: false
      }
      state.modal_alert = {
        header: '',
        header_icon: '',
        button_submit_message: '',
        subject: '',
        message: '',
        color: 'default',
        open: false
      }
    }
  },
  actions: {
    openModal: function ({ commit }, modalObject) {
      if (modalObject.type === 'form') {
        commit('triggerModalForm', modalObject)
      } else if (modalObject.type === 'alert') {
        commit('triggerModalAlert', modalObject)
      }
    },
    closeModal: function ({ commit }) {
      commit('clearModalObjects')
    }
  }
})
