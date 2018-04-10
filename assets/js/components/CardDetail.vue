<template>
  
  <div id="flashcard-detail" class="col-xl-5">
    <div class="sticky">
      <h4>Front / Back</h4>
      <textarea class="form-control" id="detail-front">{{activeCard.front}}</textarea>
      <textarea class="form-control" id="detail-back">{{activeCard.back}}</textarea>
      <div class="checkboxes">
        <input type="checkbox" value="" id="front-first">
        <label class="form-check-label" for="frontFirst">
          Always front first
        </label>
        <input type="checkbox" value="" id="marked">
        <label class="form-check-label" for="marked">
          Marked
        </label>
      </div>
    </div>
  </div>
        
</template>

<script>
  import { state } from '../index.js';
  
  export default {
    data () {
      return {}
    },
    computed: {
      activeCard: function() {
        if(state.activeCard == null) return {};
        return state.activeCard;
      }
    }
  }
</script>
