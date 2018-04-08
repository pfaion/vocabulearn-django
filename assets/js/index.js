import Vue from 'vue';

import App from './components/App.vue';
import MainMenu from './components/MainMenu.vue';

Vue.component('app', App);
Vue.component('main-menu', MainMenu);

const app = new Vue({
    el: '#app',
    render: h => h(App)
});