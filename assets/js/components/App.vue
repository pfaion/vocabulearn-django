<template>
  <div id="main-app">
    <div id="app-body" class="container">
      <h1 id="banner"><a href="/">Vocabulearn</a></h1>
      <main-menu/>
      <div id="content" class="row">
        <box class="col-xl-3"/>
        <cards class="col-xl-4"/>
        <card-detail class="col-xl-5"/>
      </div>
    </div>
    <modal/>
  </div>
</template>

<script> 
  import MainMenu from './MainMenu.vue';
  import Box from './Box.vue';
  import Cards from './Cards.vue';
  import CardDetail from './CardDetail.vue';
  import Modal from './Modal.vue';
  
  import { getCookie, setCookie } from 'tiny-cookie';
  
  import { state } from '../index.js';
  
  export default {
    data () {
      return state.$data;
    },
    watch: {
      activeSet: function(val) {
        if(val == null) return;
        setCookie('activeSet', val);
      }
    },
    created() {
      if(state.activeSet == null && getCookie('activeSet') != null) {
        state.activeSet = getCookie('activeSet');
      }
    },
    components: {
      'main-menu': MainMenu,
      'box': Box,
      'cards': Cards,
      'card-detail': CardDetail,
      'modal': Modal
    }
  }
</script>

<style lang="scss">
  @import "~style/main";
</style>
