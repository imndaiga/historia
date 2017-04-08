import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    alert: {
      message: '',
      type: '',
      duration: 0,
      dismissable: false
    }
  },
  mutations: {
    SET_ALERT: function (state, alertObject) {
      state.alert = alertObject
    }
  },
  actions: {
    alert: function ({ commit }, { message, type, duration, dismissable }) {
      return commit('SET_ALERT', {
        message: message,
        type: type,
        duration: duration,
        dismissable: dismissable
      })
    },
    dismiss_alert: function ({ commit }) {
      return commit('SET_ALERT', {
        message: '',
        type: '',
        duration: 0,
        dismissable: false
      })
    }
  }
})

export default store
