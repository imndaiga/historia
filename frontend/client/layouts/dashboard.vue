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
            type: 'footer_button',
            caption: 'Log Out',
            action: 'logout',
            class: 'btn btn-block btn-lg btn-default',
            reference: 'Your Profile',
            key: 1
          },
          {
            type: 'footer_link',
            path_type: 'internal',
            caption: 'Info',
            icon: 'fa fa-info-circle fa-fw',
            link: 'relationships',
            reference: 'Read more about the miminani project',
            key: 2
          },
          {
            type: 'footer_link',
            path_type: 'external',
            caption: 'Github',
            icon: 'fa fa-github-alt fa-fw',
            link: 'https://github.com/squarenomad/miminani',
            reference: 'View our open source code',
            key: 3
          }
        ]
      }
    }
  }
</script>

<style scoped>
</style>
