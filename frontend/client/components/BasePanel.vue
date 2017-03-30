<template>
  <div class="panel panel-default">
    <ul class="nav">
      <li :class="['panel-title', {'active': panel.open}]">
        <a v-on:click="togglePanel(panel)">
          <i :class="panel.icon"></i>
          <span>{{panel.label}}</span>
        </a>
      </li>
    </ul>
    <div class="panel-collapse collapse" :class="{'in': panel.open}">
      <div class="panel-body">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      panel: {
        type: Object,
        required: true
      }
    },
    methods: {
      togglePanel: function (PanelObject) {
        PanelObject.open = !PanelObject.open
      }
    }
  }
</script>

<style scoped>
  .panel {
    margin: 10px
  }

  .nav {
    padding: 0px 0px;
    cursor: pointer
  }

  i {
    padding-right: 30px
  }

  .nav > .active > a,
  .nav > .active > a:hover,
  .nav > .active > a:focus {
    color: #fff;
    background-color: #91acc3;
    border-radius: 3px 3px 0px 0px
  }
</style>
