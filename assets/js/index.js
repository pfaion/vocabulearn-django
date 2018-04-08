import Vue from 'vue';

import App from './components/App.vue';

const app = new Vue({
    el: '#app',
    components: {
      'app': App
    },
    render: h => h(App)
});