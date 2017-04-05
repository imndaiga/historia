<template>
  <div class="well">
    <div class="row">
      <div class="col-lg-2 col-md-3 col-sm-5 hidden-xs">
        <span class="actions-bar-title">Quick Actions</span>
      </div>
      <div class="col-lg-10 col-md-9 col-sm-7 col-xs-12">
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
    line-height: 45px;
    font-weight: 600;
    margin-left: 10px;
    font-size: 17px
  }

  i {
    font-size: 20px;
    margin-right: 10px
  }

  button {
    font-size: 15px
  }

  @media (min-width: 1200px) {
    .well {
      margin: 20px;
      padding: 19px;
      border: 1px solid #e3e3e3;
      border-radius: 4px;
      box-shadow: inset 0 1px 1px rgba(0,0,0,.05)
    }
  }

  @media (max-width: 767px) {
    .well {
      margin: 10px;
      padding: 0px;
      border: none;
      border-radius: 0px;
      box-shadow: none
    }
  }
</style>
