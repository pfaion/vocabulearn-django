<template>
  <li>
    <div class="set-badge"
      :class="{'alert-primary': isActive}"
      v-on:click="setActive">
      
      <div class="spacer"></div>
      <div class="label">{{name}}</div>
      <div class="more">
        <span class="material-icons icon-smaller">more_horiz</span>
      </div>
    </div>
  </li>
</template>

<script>

  import { state } from '../index.js';
  
  export default {
    data () {
      return {
        
      }
    },
    props: {
      name: String,
      id: Number
    },
    computed: {
      isActive: function() {
        if(state.activeSet == null) return false;
        return this.id == state.activeSet;
      }
    },
    methods: {
      setActive: function() {
        state.activeSet = this.id;
      }
    }
  }
</script>
