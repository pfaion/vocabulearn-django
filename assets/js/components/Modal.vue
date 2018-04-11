<template>
  
  <div class="modal" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{title}}</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span class="material-icons icon-small">close</span>
          </button>
        </div>
        <div class="modal-body">
          <form
            @submit.prevent="submit()">
            <div class="form-group">
              <label>{{fieldName}}</label>
              <input type="text" class="form-control" v-model="fieldContent">
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary" @click="submit()">{{buttonText}}</button>
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
        </div>
      </div>
    </div>
  </div>
    
</template>

<script>

  import { state } from '../index.js';
  
  export default {
    data () {
      return {
        title: "",
        fieldName: "",
        fieldDefault: "",
        fieldContent: "",
        buttonText: "",
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
      init(title, fieldName, buttonText, fieldDefault="") {
        this.title = title;
        this.fieldName = fieldName;
        this.buttonText = buttonText;
        this.fieldDefault = fieldDefault;
        this.fieldContent = this.fieldDefault;
        this.show = true;
      },
      submit() {
        this.$emit('submit', this.fieldContent);
        $(this.$el).modal('hide');
      }
    }
  }
</script>
