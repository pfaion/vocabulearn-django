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
        ></folder>
        
        <li class="box-list-item">
          <div class="box-list-badge text-secondary">
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
  
  export default {
    data () {
      return {
        folders: []
      }
    },
    components: {
      'folder': Folder
    },
    created() {
      this.fetchData()
    },
    methods: {
      fetchData() {
        axios.get('/API/folders')
          .then(response => {
            this.folders = response.data.folders
          })
      }
    }
  }
</script>
