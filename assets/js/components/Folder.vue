<template>
  <li>
    <div class="box-list-badge bg-dark text-white">
      <div class="icon">
        <span class="material-icons icon-smaller expanded">expand_more</span>
        <span class="material-icons icon-smaller collapsed hidden">chevron_right</span>
      </div>
      <div class="label">{{name}}</div>
      <div class="more">
        <span class="material-icons icon-smaller">more_horiz</span>
      </div>
    </div>
    <!-- <ul class="set-list">
      <set
        v-for="set in sets"
        :id="set.id"
        :name="set.name"
        :key="set.id"
      ></set>
      <li class="list-group-item border-0 card-set-add">
        <div class="row rounded text-secondary">
          <div class="spacer"></div>
          <div class="label">
            <span class="material-icons icon-smaller">add</span>
            <span class="add-description">Add set</span>
          </div>
          <span class="hidden folder-id">{{id}}</span>
        </div>
      </li>
    </ul> -->
  </li>
</template>


<script>
  import Set from './Set.vue';
  
  export default {
    data () {
      return {
        sets: []
      }
    },
    components: {
      'set': Set
    },
    props: {
      name: String,
      id: Number
    },
    created() {
      this.fetchData()
    },
    methods: {
      fetchData() {
        axios.get(`/API/sets/${this.id}`)
          .then(response => {
            this.sets = response.data.sets
          })
      }
    }
  }
</script>

