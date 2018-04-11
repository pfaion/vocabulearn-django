import Vue from 'vue';

import Modal from './components/Modal.vue';

export const state = new Vue({
  data: {
    activeSet: null,
    activeCard: null,
    currentModal: null,
    modalActive: false
  },
  methods: {
    getNewModal() {
      this.modalActive = true;
      var ComponentClass = Vue.extend(Modal);
      var instance = new ComponentClass();
      Vue.nextTick(function() {
        instance.$mount('#modal');
      });
      this.currentModal = instance;
      return instance;
    }
  }
});

import App from './components/App.vue';
export const app = new Vue({
    el: '#app',
    components: {
      'app': App
    },
    render: h => h(App)
});