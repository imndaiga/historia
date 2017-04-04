<template>
  <div class="well">
    <div class="row">
      <div class="col-lg-2 col-md-3 col-sm-4 hidden-xs">
        <span class="actions-bar-title">Quick Actions</span>
      </div>
      <div class="col-lg-10 col-md-9 col-sm-8 col-xs-12">
        <div class="btn-group btn-group-justified">
          <div v-for="button in buttons" class="btn-group">
            <button class="btn btn-lg btn-default" v-on:click="performAction(button.action)">
              <i :class="button.icon"></i>
              <span class="hidden-xs hidden-sm">{{ button.message }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      title: {
        type: String,
        required: true
      },
      buttons: {
        type: Array,
        required: true
      }
    },
    methods: {
      performAction: function (actionTrigger) {
        this.$nuxt.$emit(actionTrigger)
      }
    }
  }
</script>

<style scoped>
  .well {
    margin: 20px;
    background-color: #fff
  }
  .actions-bar-title {
    line-height: 45px
  }
  i {
    font-size: 15px
  }
</style>
