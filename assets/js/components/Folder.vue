<template>
  <li>
    
    <div v-on:click="toggleExpand" class="folder-badge bg-dark text-white">
      <div class="icon">
        <span class="material-icons icon-smaller">{{iconType}}</span>
      </div>
      <div class="label">{{name}}</div>
      <div class="more">
        <span class="material-icons icon-smaller">more_horiz</span>
      </div>
    </div>
    
    <ul v-if="expanded" class="set-list list-group">
      
      <set class="box-list-item"
        v-for="set in sets"
        :id="set.id"
        :name="set.name"
        :key="set.id"
      ></set>
      
      <li class="box-list-item">
        <div class="add-set-badge text-secondary">
          <div class="spacer"></div>
          <div class="label">
            <span class="material-icons icon-smaller">add</span>
            <span class="add-description">Add set</span>
          </div>
        </div>
      </li>
      
    </ul>
    
  </li>
</template>


<script>
  import Set from './Set.vue';
  import { getCookie, setCookie } from 'tiny-cookie';
  
  export default {
    data () {
      return {
        expanded: false,
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
    computed: {
      iconType: function() {
        return this.expanded ? "chevron_right" : "expand_more";
      },
      cookieName: function() {
        return `folder-${this.id}-expanded`;
      }
    },
    watch: {
      expanded: function(val) {
        setCookie(this.cookieName, val);
      }
    },
    created() {
      if(getCookie(this.cookieName) != null) {
        this.expanded = (getCookie(this.cookieName) == 'true');
      }
      this.fetchData();
    },
    methods: {
      fetchData() {
        axios.get(`/API/sets/${this.id}`)
          .then(response => {
            this.sets = response.data.sets
          })
      },
      toggleExpand() {
        this.expanded = !this.expanded;
      }
    }
  }
</script>

