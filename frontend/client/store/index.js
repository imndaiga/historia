import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    alert: {},
    authUser: null
  },
  mutations: {
    SET_ALERT: function (state, alertObject) {
      state.alert = alertObject
    },
    SET_USER: function (state, userProfile) {
      state.authUser = userProfile
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
    },
    login: function ({ commit }, { email }) {
      return commit('SET_USER', email)
    },
    logout: function ({ commit }) {
      return commit('SET_USER', null)
    }
  }
})

export default store
