<template>

  <div class="row border"
    :class="{'list-group-item-primary': isActive}"
    v-on:click="setActive">
    <span class="list-number">{{i}}</span>
    <span class="front_short">{{card.front}}</span>
    <span class="back_short">{{card.back}}</span>
    <div class="delete-card-button rounded">
      <span class="material-icons icon-small">delete</span>
    </div>
  </div>
  
</template>

<script>
  import { state } from '../index.js';
  
  export default {
    data () {
      return {}
    },
    props: [
      'i',
      'card'
    ],
    computed: {
      isActive: function() {
        if(state.activeCard == null) return false;
        return this.card.id == state.activeCard.id;
      }
    },
    methods: {
      setActive() {
        console.log("test");
        state.activeCard = this.card;
      }
    }
  }
</script>
