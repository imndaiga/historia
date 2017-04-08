<template>
  <div>
    <div class='jumbotron'>
      <img src="~assets/img/logo.png" alt="jina" class="logo" width="80" height="94" style="display: block; margin: auto; position: relative; z-index: 1;"/>
      <div id='particlesjs'></div>
      <div class='container-fluid'>
        <div class='welcome-banner row'>
          <div class='col-lg-7 col-md-8 col-sm-8 col-xs-12 col-lg-push-1 col-md-push-1 col-sm-push-1'>
            <div>
              <p class="header"><em>Connecting</em> African Histories.</p>
              <p class="intro">History is a collection of stories. We help you tell yours.</p>
              <hr>
              <p class='welcome-action'>
                <a class='btn btn-success btn-lg' v-on:click='login()'>Tell your story</a>
                <a href='#'>
                  <i class='fa fa-external-link fa-fw'></i>
                  Learn more
                </a>
              </p>
            </div>
          </div>
        </div>
        <base-modal-form></base-modal-form>
      </div>
    </div>
    <footer class='footer'>
      <div class='container'>
        <span class='text-muted'>
          <small>&copy; 2017 squarenomad.com</small>
        </span>
      </div>
    </footer>
  </div>
</template>

<script>
  import BaseModalForm from '~components/BaseModalForm.vue'
  var PJSConf = require('~static/particlesjs.json')
  if (process.browser) {
    require('particles.js')
  }
  export default {
    components: {
      BaseModalForm: BaseModalForm
    },
    data: function () {
      return {
        login_form: {
          data: [
            {
              type: 'email-input',
              placeholder: 'Enter Email Address',
              label: 'Email',
              validators: ['required', 'email'],
              field_name: 'email',
              classes: '',
              key: 1
            },
            {
              type: 'password-input',
              placeholder: 'Enter Password',
              label: 'Password',
              validators: ['required'],
              field_name: 'password',
              classes: '',
              key: 2
            }
          ],
          modal_title: 'Login',
          modal_icon: 'fa fa-sign-in fa-fw',
          modal_submit_message: 'Log In',
          inline: false,
          resource_urls: {
            submit_url: 'login',
            search_url: ''
          }
        }
      }
    },
    mounted: function () {
      window.particlesJS('particlesjs', PJSConf)
    },
    methods: {
      login: function () {
        this.$nuxt.$emit('open-modal', JSON.stringify(this.login_form))
      }
    }
  }
</script>

<style scoped>
  .jumbotron {
    position: relative;
    height: calc(100vh - 60px)
  }

  .welcome-action {
    padding-top: 10px;
  }
  .welcome-action > a {
    margin-right: 20px
  }

  .welcome-action > a:last-child,
  .welcome-action > a:last-child:hover,
  .welcome-action > a:last-child:focus {
    color: grey;
    font-size: 18px;
    text-decoration: none
  }

  .welcome-banner {
    padding-top: 40px
  }

  #particlesjs {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #c2dcc8;
    z-index: 0
  }

  .footer {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    /* Set the fixed height of the footer here */
    height: 60px;
    line-height: 59px; /* Vertically center the text there */
    background-color: #f5f5f5
  }

  .header {
    font-size: 45px
  }

  .intro {
    font-size: 30px
  }
</style>
