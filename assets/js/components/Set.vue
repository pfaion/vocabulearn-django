<template>
  <li class="list-group-item border-0 card-set">
    <a>
    <!-- <a href="/set/{{set.id}}"> -->
      <div class="row rounded {% if set.id == set_id %} alert-primary {% endif %}">
        <div class="spacer"></div>
        <div class="label">{{name}}</div>
        <div class="more">
          <span class="material-icons icon-smaller">more_horiz</span>
        </div>
      </div>
      
    </a>
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
