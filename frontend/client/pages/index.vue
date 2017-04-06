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
  export default {
    head: function () {
      return {
        script: [
          { src: 'https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js' }
        ]
      }
    },
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
        },
        particlesjs_data: {
          'particles': {
            'number': {
              'value': 30,
              'density': { 'enable': true, 'value_area': 800 }
            },
            'color': { 'value': '#ffffff' },
            'shape': {
              'type': 'circle',
              'stroke': { 'width': 0, 'color': '#000000' },
              'polygon': { 'nb_sides': 5 },
              'image': {
                'src': 'img/github.svg',
                'width': 100,
                'height': 100
              }
            },
            'opacity': {
              'value': 0.5,
              'random': false,
              'anim': {
                'enable': false,
                'speed': 1,
                'opacity_min': 0.1,
                'sync': false
              }
            },
            'size': {
              'value': 10,
              'random': true,
              'anim': {
                'enable': false,
                'speed': 80,
                'size_min': 0.1,
                'sync': false
              }
            },
            'line_linked': {
              'enable': true,
              'distance': 300,
              'color': '#ffffff',
              'opacity': 0.4,
              'width': 2
            },
            'move': {
              'enable': true,
              'speed': 3,
              'direction': 'none',
              'random': false,
              'straight': false,
              'out_mode': 'out',
              'bounce': false,
              'attract': {
                'enable': false,
                'rotateX': 600,
                'rotateY': 1200
              }
            }
          },
          'interactivity': {
            'detect_on': 'canvas',
            'events': {
              'onhover': { 'enable': false, 'mode': 'repulse' },
              'onclick': { 'enable': true, 'mode': 'push' },
              'resize': true
            },
            'modes': {
              'grab': { 'distance': 800, 'line_linked': { 'opacity': 1 } },
              'bubble': {
                'distance': 800,
                'size': 80,
                'duration': 2,
                'opacity': 0.8,
                'speed': 3
              },
              'repulse': { 'distance': 400, 'duration': 0.4 },
              'push': { 'particles_nb': 4 },
              'remove': { 'particles_nb': 2 }
            }
          },
          'retina_detect': true
        }
      }
    },
    mounted: function () {
      window.particlesJS('particlesjs', this.particlesjs_data)
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
