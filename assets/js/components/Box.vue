<template>
  <div id="box">
    <div class="sticky">
      <h4>Box</h4>
      <ul id="folder-list" class="list-group small">
        
        <folder class="box-list-item"
          v-for="folder in folders"
          :id="folder.id"
          :name="folder.name"
          :key="folder.id"
          v-on:ready="registerReady(folder.id)"
          ref="folders"
        ></folder>
        
        <li class="box-list-item">
          <div class="add-folder-badge text-secondary">
            <div class="icon">
              <span class="material-icons icon-smaller">add</span>
            </div>
            <div class="label">Add folder</div>
          </div>
        </li>
        
      </ul>
    </div>
  </div>
</template>


<script>
  import Folder from './Folder.vue';
  
  import { state } from '../index.js';
  
  export default {
    data () {
      return {
        folders: [],
        foldersReady: []
      }
    },
    watch: {
      foldersReady: function(val) {
        if(this.folders.length != this.foldersReady.length) return;
        if(state.activeSet != null) return;
        if(this.folders.length == 0) return;
        this.makeFirstSetActive();
      }
    },
    components: {
      'folder': Folder
    },
    created() {
      this.fetchData();
    },
    methods: {
      fetchData() {
        axios.get('/API/folders')
          .then(response => {
            this.folders = response.data.folders;
          });
      },
      registerReady(id) {
        if(_.includes(this.foldersReady, id)) return;
        this.foldersReady.push(id);
      },
      makeFirstSetActive() {
        for (var i = 0; i < this.$refs.folders.length; i++) {
          var folder = this.$refs.folders[i];
          if(folder.sets.length == 0) continue;
          state.activeSet = folder.sets[0].id;
          break;
        }
      }
    }
  }
</script>
