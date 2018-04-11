<template>
  <li>
    
    <div @click="toggleExpand" class="folder-badge bg-dark text-white">
      <div class="icon">
        <span class="material-icons icon-smaller">{{iconType}}</span>
      </div>
      <div class="label">{{name}}</div>
      <div class="more" @click.stop="showEditModal = true">
        <span class="material-icons icon-smaller">more_horiz</span>
      </div>
    </div>
    
    <modal v-if='showEditModal'
      :title="'Edit Folder'"
      :fieldName="'Name'"
      :fieldContent="name"
      :buttonText="'Edit'"
      @closed="showEditModal = false"
      @submit="editFolder"
    />
    
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
  import Modal from './Modal.vue';
  import { getCookie, setCookie } from 'tiny-cookie';
  
  import { state } from '../index.js';
  
  export default {
    data () {
      return {
        expanded: false,
        sets: [],
        showEditModal: false
      }
    },
    components: {
      'set': Set,
      'modal': Modal
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
      },
      hasActiveSet: function() {
        if(state.activeSet == null) return false;
        return _.some(this.sets, ['id', state.activeSet]);
      }
    },
    watch: {
      expanded: function(val) {
        setCookie(this.cookieName, val);
      },
      hasActiveSet: function(val) {
        if(val) this.expanded = true;
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
            this.sets = response.data.sets;
            this.$emit('ready');
          })
      },
      toggleExpand() {
        if(this.hasActiveSet) return;
        this.expanded = !this.expanded;
      },
      editFolder() {
        console.log('edit folder');
      }
    }
  }
</script>

