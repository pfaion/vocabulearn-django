<template>

  <div id="cards" class="col-xl-4">
    <h4>Cards (<span id="card-count">{{cards.length}}</span>)</h4>
    <div id="flashcard-list" class="small">
      <card
        v-for="(card, i) in cards"
        :i="i"
        :card="card"
        :key="card.id"
        >
      </card>
    </div>
  </div>
  
</template>

<script>

  import Card from './Card.vue';
  
  import { state } from '../index.js';
  
  export default {
    data () {
      return {
        cards: []
      }
    },
    computed: {
      activeSet: function() {
        return state.activeSet;
      }
    },
    watch: {
      activeSet: function(val) {
        this.fetchData();
      }
    },
    created() {
      this.fetchData();
    },
    methods: {
      fetchData () {
        if(this.activeSet == null) return;
        axios.get(`/API/cards-for-set/${this.activeSet}/`)
          .then(response => {
            this.cards = response.data.cards;
            state.activeCard = this.cards[0];
          })
      }
    },
    components: {
      'card': Card
    }
  }
</script>
