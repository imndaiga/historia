<template>
  <div>
    <div class="col-lg-10 col-lg-push-2 col-md-9 col-md-push-3 col-sm-8 col-sm-push-4 col-xs-12">
      <alert-message></alert-message>
    </div>
    <nuxt/>
    <base-sidebar class="hidden-xs" :pages="pages" :footer="footer"></base-sidebar>
    <base-mobile-menu class="hidden-lg hidden-md hidden-sm" :pages="pages" :footer="footer"></base-mobile-menu>
  </div>
</template>

<script>
  import BaseSidebar from '~components/BaseSidebar.vue'
  import BaseMobileMenu from '~components/BaseMobileMenu.vue'
  import AlertMessage from '~components/AlertMessage.vue'
  export default {
    components: {
      BaseSidebar: BaseSidebar,
      BaseMobileMenu: BaseMobileMenu,
      AlertMessage: AlertMessage
    },
    data: function () {
      return {
        pages: [
          {
            name: 'user',
            navs: [
              {
                title: 'home',
                info: 'View your progress',
                view: 'user-home',
                icon: 'fa fa-home fa-fw',
                key: 1
              },
              {
                title: 'settings',
                info: 'Configure your profile settings',
                view: 'user-settings',
                icon: 'fa fa-cog fa-fw',
                key: 2
              },
              {
                title: 'sign out',
                info: 'Log out of your account',
                action: 'logout',
                icon: 'fa fa-sign-out fa-fw',
                key: 3
              }
            ],
            icon: 'fa fa-user-circle-o fa-lg',
            key: 1
          },
          {
            name: 'visualisation',
            navs: [],
            icon: 'fa fa-eye fa-lg',
            key: 2
          },
          {
            name: 'relationships',
            navs: [],
            icon: 'fa fa-globe fa-lg',
            key: 3
          }
        ],
        footer: [
          {
            type: 'footer_link',
            path_type: 'internal',
            caption: 'Info',
            icon: 'fa fa-info-circle fa-fw fa-lg',
            link: 'relationships',
            reference: 'Read more about the miminani project',
            key: 1
          },
          {
            type: 'footer_link',
            path_type: 'external',
            caption: 'Github',
            icon: 'fa fa-github-alt fa-fw fa-lg',
            link: 'https://github.com/squarenomad/miminani',
            reference: 'View our open source code',
            key: 2
          }
        ]
      }
    }
  }
</script>

<style scoped>
</style>
