<template>
  <div class="menu">
    <ul class="nav nav-app-brand">
      <img src="~assets/img/logo.png" alt="jina" class="logo" width="65" height="77" />
    </ul>
    <ul class="nav nav-app-menu">
      <router-link v-for="page in pages" v-if="page.navs.length == 0" :to="{name: page.name}" tag="li" active-class="active" :key="page.key" v-on:click.native="setOpenMenu(page.name)">
        <a>
          <i :class="page.icon"></i>
          {{page.name}}
        </a>
      </router-link>
      <li v-else-if="page.navs.length > 0" :key="page.key" :class="{'active': current_Page == page.name}">
        <a v-on:click="setOpenMenu(page.name)">
          <i :class="page.icon"></i>
          {{page.name}}
          <span class="fa fa-chevron-down fa-fw reveal-icon"></span>
        </a>
        <ul :class="['nav', 'nav-app-submenu', 'collapse', {'in': open_submenu == page.name}]">
          <router-link v-for="menu in page.navs" v-if="menu.view" :to="{name: menu.view}" tag="li" active-class="active" :key="menu.key" v-on:click.native="setOpenMenu(page.name)">
            <a>
            <i :class="menu.icon"></i>
            {{menu.title}}
            </a>
          </router-link>
          <li v-else>
            <a v-on:click="performAction(menu.action)">
              <i :class="menu.icon"></i>
              {{menu.title}}
            </a>
          </li>
        </ul>
      </li>
    </ul>
    <div class="nav-app-footer">
      <button type="button" v-for="item in footer" v-if="item.type == 'footer_button'" :class="item.class" v-on:click="performAction(item.action)">{{item.caption}}</button>
      <ul class="list-inline">
        <router-link v-for="item in footer" v-if="item.path_type == 'internal'" active-class="active" :to="{name: item.link}" tag="li" :key="item.key">
          <a :class="item.icon"></a>
        </router-link>
        <li v-else-if="item.path_type == 'external'">
          <a :href="item.link" :class="item.icon"></a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      pages: {
        type: Array,
        required: true
      },
      footer: {
        type: Array,
        required: true
      }
    },
    data: function () {
      return {
        open_submenu: this.current_Page
      }
    },
    methods: {
      performAction: function (action) {
        var loggedOutAlert = {
          message: 'You have been logged out',
          type: 'alert-warning',
          dismissable: false,
          duration: 0
        }
        if (action === 'logout') {
          var self = this
          this.logout()
          this.$nuxt.$router.push('/', function () {
            self.$nuxt.$store.dispatch('alert', loggedOutAlert)
          })
        }
      },
      setOpenMenu: function (pageName) {
        this.open_submenu = pageName
      }
    },
    computed: {
      current_Page: function () {
        return this.$nuxt.$route.name.split('-')[0]
      }
    }
  }
</script>

<style scoped>
  .nav-app-brand {
    margin-top: 10px;
    margin-bottom: 30px;
    font-size: 150%;
    text-align: center;
    cursor: pointer;
    padding-bottom: 15px;
    border-bottom: 1px solid #eee
  }

  .nav-app-menu {
    margin-right: -21px; /* 20px padding + 1px border */
    margin-bottom: 0px;
    margin-left: -20px;
    border-bottom: 2px solid #eee
  }
  .nav-app-menu > li {
    cursor: pointer
  }
  .nav-app-menu > li > a {
    padding-left: 20px;
    font-size: 16px;
    font-weight: 400;
    line-height: 50px;
    text-transform: capitalize;
    color:  rgba(100, 100, 100, 1);
  }
  .nav-app-menu > .active > a,
  .nav-app-menu > .active > a:hover,
  .nav-app-menu > .active > a:focus {
    color: #fff;
    background-color: #428bca
  }
  .nav-app-menu > li > a > i {
    padding-right: 15px;
    color: #525252;
    font-size: 25px
  }
  .nav-app-menu > .active > a > i,
  .nav-app-menu > .active > a > .reveal-icon {
    color: #fff;
  }
  .nav-app-menu > li > a > .reveal-icon {
    position: absolute;
    right: 20px;
    top: 25px;
    color:  rgba(150, 150, 150, 0.5)
  }

  .nav-app-submenu {
    background-color: #dad4d4
  }
  .nav-app-submenu > li > a {
    padding-left: 40px;
    font-size: 14px;
    line-height: 20px;
    text-transform: capitalize;
    color:  rgba(100, 100, 100, 1);
    border-bottom: 1px solid rgba(150, 150, 150, 0.2)
  }
  .nav-app-submenu > li > a:hover {
    background-color: #cbcbd2
  }
  .nav-app-submenu > .active > a,
  .nav-app-submenu > .active > a:hover,
  .nav-app-submenu > .active > a:focus {
    color: #fff;
    background-color: #91acc3
  }
  .nav-app-submenu > li > a > i {
    font-size: 19px;
    padding-right: 35px
  }

  .nav-app-footer {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 10px 10px 0px 10px;
    background-color: rgba(214, 214, 214, 1)
  }
  .nav-app-footer > ul {
    margin-top: 5px;
    margin-left: calc(50% - 35px)
  }
  .nav-app-footer > ul > li > a,
  .nav-app-footer > ul > li > a:hover,
  .nav-app-footer > ul > li > a:focus {
    color: #525252;
    text-decoration: none
  }

  /* Landscape phones and portrait tablets */
  @media (max-width: 767px) {
    .menu {
      position: relative
    }
    .nav-app-footer {
      height: 100px;
      bottom: -100px;
      left: -21px;
      right: -21px
    }
  }

    /* Portrait phones and smaller */
  @media (max-width: 480px) {
    .menu {
      position: static
    }
    .nav-app-footer {
      height: auto;
      bottom: 0;
      left: 0;
      right: 0
    }
  }
</style>
