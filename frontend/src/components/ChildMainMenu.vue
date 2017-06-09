<template>
  <div class="menu">
    <ul class="nav nav-app-brand">
      <img src="../assets/logo.png" alt="jina" class="logo" width="93" height="77" />
    </ul>
    <ul class="nav nav-app-menu">
      <router-link v-for="page in pages" v-if="page.navs.length === 0" :to="{name: page.view}" tag="li" active-class="active" :key="page.key" v-on:click.native="setOpenMenu(page.title)">
        <a>
          <icon :name="page.icon"></icon>
          <span class="nav-title">{{page.title}}</span>
        </a>
      </router-link>
      <li v-else-if="page.navs.length > 0" :key="page.key" :class="{'active': current_Page.parent === page.title}">
        <a v-on:click="setOpenMenu(page.title)">
          <icon :name="page.icon" ></icon>
          <span class="nav-title">{{page.title}}</span>
          <icon name="chevron-down" class="reveal-icon"></icon>
        </a>
        <ul :class="['nav', 'nav-app-submenu', 'collapse', {'in': open_submenu === page.title}]">
          <router-link v-for="menu in page.navs" v-if="menu.view" :to="{name: menu.view}" tag="li" active-class="active" :key="menu.key" v-on:click.native="setOpenMenu(page.title)">
            <a>
              <icon :name="menu.icon"></icon>
              <span class="nav-title">{{menu.title}}</span>
            </a>
          </router-link>
          <li v-else>
            <a v-on:click="performAction(menu.action)">
              <icon :name="menu.icon"></icon>
              <span class="nav-title">{{menu.title}}</span>
            </a>
          </li>
        </ul>
      </li>
    </ul>
    <div class="nav-app-footer">
      <button type="button" v-for="item in footer" v-if="item.type === 'footer_button'" :class="item.class" v-on:click="performAction(item.action)">{{item.caption}}</button>
      <ul class="list-inline">
        <router-link v-for="item in footer" v-if="item.path_type === 'internal'" active-class="active" :to="{name: item.link}" tag="li" :key="item.key">
          <a>
            <icon :name="item.icon"></icon>
          </a>
        </router-link>
        <li v-else-if="item.path_type === 'external'">
          <a :href="item.link">
            <icon :name="item.icon"></icon>
          </a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
  import 'vue-awesome/icons'
  import auth from '@/utils/auth'
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
        open_submenu: ''
      }
    },
    methods: {
      performAction: function (action) {
        if (action === 'logout') {
          auth.logout()
          this.$router.push('/')
        }
      },
      setOpenMenu: function (pageName) {
        this.open_submenu = pageName
      }
    },
    computed: {
      current_Page: function () {
        return {
          name: this.$route.name,
          parent: this.$route.path.split('/').slice(-2)[0]
        }
      }
    }
  }
</script>

<style scoped>
  .fa-icon {
    position: absolute;
  }
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
    font-size: 17px;
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
  .nav-title {
    padding-left: 25px;
  }
  .nav-app-menu > li > a > .fa-icon {
    top: 25px;
  }
  .nav-app-menu > li > a > .reveal-icon {
    right: 20px;
    color:  rgba(150, 150, 150, 0.5)
  }
  .nav-app-menu > .active > a > .reveal-icon {
    color:  #fff
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
    text-decoration: none;
    font-size: 18px;
  }
  .nav-app-footer > ul > li > a > .fa-icon {
    position: static;
  }

  /* Landscape phones and portrait tablets and smaller*/
  @media (max-width: 767px) {
    .menu {
      position: static
    }
    .nav-app-footer {
      background-color: rgba(214, 214, 214, 0)
    }
    .nav-app-footer > ul > li > a,
    .nav-app-footer > ul > li > a:hover,
    .nav-app-footer > ul > li > a:focus {
      font-size: 25px;
      padding-left: 25px
    }
    .nav-app-footer > ul > li:first-child > a {
      padding-left: 0px
    }
  }
</style>
