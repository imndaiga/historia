<template>
  <div class="well">
    <div class="row">
      <div class="col-lg-2 col-md-3 col-sm-5 hidden-xs">
        <span class="actions-bar-title">{{ title }}</span>
      </div>
      <div class="col-lg-10 col-md-9 col-sm-7 col-xs-12">
        <div class="btn-group btn-group-justified">
          <div v-for="button in buttons" class="btn-group">
            <button class="btn btn-lg btn-default" v-on:click="performAction(button.action, button.target)">
              <icon :name="button.icon"></icon>
              <span class="button-message hidden-xs hidden-sm">{{ button.message }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import bus from '../utils/bus'
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
      performAction: function (actionTrigger, actionTarget) {
        bus.$emit(actionTrigger, actionTarget)
      }
    }
  }
</script>

<style scoped>
  .fa-icon {
    width: auto;
    height: 1em;
  }

  .row {
    line-height: 45px;
    height: 45px;
  }

  .well {
    margin: 20px;
    background-color: #fff
  }

  .actions-bar-title {
    font-weight: 600;
    margin-left: 10px;
    font-size: 19px
  }

  button {
    font-size: 17px;
  }
  .button-message {
    padding-left: 15px;
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
