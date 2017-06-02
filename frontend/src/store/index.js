import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    modalIsOpen: false,
    mobileMenuIsOpen: false
  },
  mutations: {
    toggleModal: function (state) {
      state.modalIsOpen = !state.modalIsOpen
    },
    toggleMobileMenu: function (state) {
      state.mobileMenuIsOpen = !state.mobileMenuIsOpen
    }
  },
  actions: {
    openModal: function ({ commit }) {
      commit('toggleModal')
    },
    closeModal: function ({ commit }) {
      commit('toggleModal')
    },
    openMobileMenu: function ({ commit }) {
      commit('toggleMobileMenu')
    },
    closeMobileMenu: function ({ commit }) {
      commit('toggleMobileMenu')
    }
  }
})
