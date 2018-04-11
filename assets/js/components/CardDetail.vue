<template>
  
  <div id="flashcard-detail" class="col-xl-5">
    <div class="sticky">
      <h4>Front / Back</h4>
      <textarea class="form-control" id="detail-front">{{activeCard.front}}</textarea>
      <div id="history-front">
        <div 
          v-for="entry in historyFront"
          :class="{right: entry=='1', wrong: entry=='0'}">
        </div>
      </div>
      <textarea class="form-control" id="detail-back">{{activeCard.back}}</textarea>
      <div id="history-back">
        <div 
          v-for="entry in historyBack"
          :class="{right: entry=='1', wrong: entry=='0'}">
        </div>
      </div>
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
      },
      historyFront: function() {
        if(_.isEmpty(this.activeCard)) return [];
        return this.activeCard.history.split('');
      },
      historyBack: function() {
        if(_.isEmpty(this.activeCard)) return [];
        return this.activeCard.history_back.split('');
      }
    }
  }
</script>
