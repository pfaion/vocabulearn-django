import Vue from 'vue';

export const state = new Vue({
  data: {
    activeSet: null,
    activeCard: null
  }
});

import App from './components/App.vue';
const app = new Vue({
    el: '#app',
    components: {
      'app': App
    },
    render: h => h(App)
});