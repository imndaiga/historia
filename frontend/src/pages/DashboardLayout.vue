<template>
  <div>
    <div class="col-lg-10 col-lg-push-2 col-md-9 col-md-push-3 col-sm-8 col-sm-push-4 col-xs-12">
      <app-view-header class="hidden-lg hidden-md hidden-sm"></app-view-header>
      <!-- insert child views here -->
    </div>
    <app-sidebar class="hidden-xs" :pages="pages" :footer="footer"></app-sidebar>
    <app-mobile-menu class="hidden-lg hidden-md hidden-sm" :pages="pages" :footer="footer"></app-mobile-menu>
  </div>
</template>

<script>
  import ParentSidebarMenu from '@/components/ParentSidebarMenu.vue'
  import ParentMobileMenu from '@/components/ParentMobileMenu.vue'
  import AppViewHeader from '@/components/AppViewHeader.vue'
  export default {
    components: {
      AppSidebar: ParentSidebarMenu,
      AppMobileMenu: ParentMobileMenu,
      AppViewHeader: AppViewHeader
    },
    data: function () {
      return {
        pages: [
          {
            title: 'user',
            navs: [
              {
                title: 'home',
                info: 'View your progress',
                view: 'dashboard',
                icon: 'home',
                key: 1
              },
              {
                title: 'settings',
                info: 'Configure your profile settings',
                view: 'dashboard',
                icon: 'cog',
                key: 2
              },
              {
                title: 'sign out',
                info: 'Log out of your account',
                action: 'logout',
                icon: 'sign-out',
                key: 3
              }
            ],
            icon: 'user-circle-o',
            key: 1
          },
          {
            title: 'visualisation',
            view: 'dashboard',
            navs: [],
            icon: 'eye',
            key: 2
          },
          {
            title: 'relationships',
            view: 'dashboard',
            navs: [],
            icon: 'globe',
            key: 3
          }
        ],
        footer: [
          {
            type: 'footer_link',
            path_type: 'internal',
            caption: 'Info',
            icon: 'info-circle',
            view: 'dashboard',
            reference: 'Read more about the miminani project',
            key: 1
          },
          {
            type: 'footer_link',
            path_type: 'external',
            caption: 'Github',
            icon: 'github-alt',
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
