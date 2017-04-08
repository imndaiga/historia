import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    alert: {}
  },
  mutations: {
    SET_ALERT: function (state, alertObject) {
      state.alert = alertObject
    }
  },
  actions: {
    alert: function ({ commit }, { message, type, duration, dismissable }) {
      return commit('SET_ALERT', {
        message: message || '',
        type: type || 'alert-info',
        duration: duration || 0,
        dismissable: dismissable || false
      })
    },
    dismiss_alert: function ({ commit }) {
      return commit('SET_ALERT', {})
    }
  }
})

export default store
