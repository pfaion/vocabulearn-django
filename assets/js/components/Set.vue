<template>
  <li>
    <div class="set-badge">
      <div class="spacer"></div>
      <div class="label">{{name}}</div>
      <div class="more">
        <span class="material-icons icon-smaller">more_horiz</span>
      </div>
    </div>
  </li>
</template>

<script>

  
  export default {
    data () {
      return {
        
      }
    },
    props: {
      name: String,
      id: Number
    }
  }
</script>
