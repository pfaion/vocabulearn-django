<template>
  
  <div class="modal" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <span contenteditable="true">{{title}}</span>
            <span class="text-muted">(click to edit)</span>
          </h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span class="material-icons icon-small">close</span>
          </button>
        </div>
        <div class="modal-body">
          <img :src="'/API/plots/'+graphUrl" alt="" width="100%" />
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Ok</button>
        </div>
      </div>
    </div>
  </div>
    
</template>

<script>
  import Vue from 'vue';
  import { state } from '../index.js';
  
  export default {
    data () {
      return {
        title: "",
        graphUrl: "",
        show: false,
        isMounted: false
      }
    },
    computed: {
      shouldShow: function() {
        return this.isMounted && this.show;
      }
    },
    watch: {
      shouldShow: function(val) {
        if(val) $(this.$el).modal('show');
      }
    },
    created() {
      console.log("created");
      state.modalActive = true;
      var modal = this;
      Vue.nextTick(function() {
        modal.$mount('#modal');
      });
    },
    mounted() {
      var modal = this;
      $(this.$el).on('hidden.bs.modal', function(event) {
        modal.$emit('closed');
        modal.$destroy();
      });
      this.isMounted = true;
    },
    destroyed() {
      state.modalActive = false;
    },
    methods: {
      init(title, graphUrl) {
        this.title = title;
        this.graphUrl = graphUrl;
        this.show = true;
      }
    }
  }
</script>
