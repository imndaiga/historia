<template>
  <div>
    <actions-bar :title="actions_bar_title"  :buttons="action_buttons" :styles="actions_bar_style"></actions-bar>
    <card :header="'Welcome ' + user.nickname + '!'" headerIcon="user">
      <ul class="list-group">
        <li class="list-group-item list-group-item-success">
          <span>You have {{ userNodeSize }} members in your history tree!</span>
        </li>
      </ul>

    </card>
    <card bodyPadding="0px">
      <div class="add-panel" v-on:click="AddPanel">
        <icon name="plus"></icon>
      </div>
    </card>
  </div>
</template>

<script>
  import AppActionsBar from '@/components/AppActionsBar.vue'
  import AppCard from '@/components/AppCard.vue'
  import bus from '@/utils/bus'

  export default {
    components: {
      ActionsBar: AppActionsBar,
      Card: AppCard
    },
    data: function () {
      return {
        actions_bar_title: 'Quick Actions',
        action_buttons: [
          {
            message: 'Add Relative',
            icon: 'link',
            action: 'open-modal',
            target: 'relative_form',
            key: 1
          },
          {
            message: 'Add Relationship',
            icon: 'user-plus',
            action: 'open-modal',
            target: 'relationship_form',
            key: 2
          }
        ],
        actions_bar_style: {
          well: 'margin: 20px; background-color: #fff; border-radius: 0px',
          row: 'line-height: 45px; height: 45px',
          titleDivClass: 'col-lg-2 col-md-3 col-sm-5 hidden-xs',
          title: 'font-weight: 600; margin-left: 10px; font-size: 19px',
          buttonDivClass: 'col-lg-10 col-md-9 col-sm-7 col-xs-12',
          button: 'font-size: 17px;'
        },
        forms: {
          relative_form: [
            {
              type: 'search-input',
              placeholder: 'Search for Relative',
              label: 'From',
              validators: ['required'],
              field_name: 'from_person',
              classes: '',
              SelectLabel: '',
              DeselectLabel: '',
              key: 1
            },
            {
              type: 'search-input',
              placeholder: 'Search for Relative',
              label: 'To',
              validators: ['required'],
              field_name: 'to_person',
              classes: '',
              SelectLabel: '',
              DeselectLabel: '',
              key: 2
            },
            {
              type: 'multiselect-input',
              placeholder: 'Choose a Relation',
              label: 'Relation',
              validators: ['required'],
              field_name: 'relation_name',
              classes: '',
              multiselect_options: ['Parent', 'Partner', 'Sibling', 'Step-Parent', 'Step-Sibling', 'Child'],
              SelectLabel: '',
              DeselectLabel: '',
              key: 3
            }
          ],
          relationship_form: [
            {
              type: 'alpha-input',
              placeholder: 'Enter First Name',
              label: 'First Name',
              validators: ['required', 'alpha'],
              field_name: 'first_name',
              classes: '',
              key: 1
            },
            {
              type: 'alpha-input',
              placeholder: 'Enter Ethnic Name',
              label: 'Ethnic Name',
              validators: ['required', 'alpha'],
              field_name: 'ethnic_name',
              classes: '',
              key: 2
            },
            {
              type: 'alpha-input',
              placeholder: 'Enter Last Name',
              label: 'Last Name',
              validators: ['required', 'alpha'],
              field_name: 'last_name',
              classes: '',
              key: 3
            },
            {
              type: 'email-input',
              placeholder: 'Enter Email Address',
              label: 'Email',
              validators: ['email'],
              field_name: 'email',
              classes: '',
              key: 4
            },
            {
              type: 'pikaday-input',
              placeholder: 'Select Birth Date',
              label: 'Date of Birth',
              field_name: 'birth_date',
              classes: '',
              key: 8
            }
          ]
        },
        user: JSON.parse(localStorage.getItem('profile')),
        userNodeSize: {}
      }
    },
    created: function () {
      this.getData()
      bus.$on('open-modal', function (modalInput) {
        var header = 'Edit'
        var icon = 'edit'
        for (var index in this.action_buttons) {
          if (this.action_buttons[index].target === modalInput) {
            icon = this.action_buttons[index].icon
            header = this.action_buttons[index].message
          }
        }
        bus.$emit('modal-data-ready', header, icon, this.forms[modalInput], 'Save', null)
      }.bind(this))
    },
    methods: {
      AddPanel: function () {
        bus.$emit('modal-data-ready', 'Pin History', 'thumb-tack', null, null, 'Under development!', null, null)
      },
      getData: function () {
        var self = this
        this.$http.get('api/user/statistics')
        .then(function (reponse) {
          self.userNodeSize = reponse.data.nodeSize
        }).catch(function (error) {
          console.log(error)
          bus.$emit('modal-data-ready', 'Ooops!', 'exclamation-circle', null, null, 'An error occured!', 'Something went wrong while retrieving data.', 'red')
        })
      }
    }
  }
</script>

<style scoped>
  .add-panel {
    font-size: 60px;
    text-align: center;
    color: lightgrey;
    cursor: pointer;
    min-height: 120px;
    padding-top: 7%
  }
  .add-panel:focus,
  .add-panel:hover {
    color: grey;
    background-color: #f5f5f5;
  }
</style>
