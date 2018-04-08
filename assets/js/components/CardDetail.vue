<template>
  
  <div id="flashcard-detail" class="col-xl-5">
    <div class="sticky">
      <h4>Front / Back</h4>
      <textarea class="form-control" id="detail-front"> </textarea>
      <textarea class="form-control" id="detail-back"> </textarea>
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
  
  export default {
    data () {
      return {}
    }
  }
</script>
