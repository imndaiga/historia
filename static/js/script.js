Vue.component('app-panel', {
	template: '#app-panel',
	props: {
		header: {
			type: String,
			required: true
		},
		menus: {
			type: Array
		},
		panel_list: {
			type: Array,
			required: true
		}
	}
});

Vue.component('app-navbar', {
	template: '#app-navbar',
	props: {
		title: {
			type: String,
			required: true
		},
		menus: {
			type: Array,
			required: true
		}
	}
});

Vue.component('app-sidebar', {
	template: "#app-sidebar",
	props: {
		panels: {
			type: Array,
			required: true
		}
	}
});

var vm = new Vue({
	el: '#app',
	data: {
		panel_list: [
			'Overview',
			'Relationships',
			'Visualisation',
			'Share'
		],
		menu_items: [
			{
				caption: 'Info',
				icon: 'fa fa-info-circle fa-lg',
				link: '#',
				class: '',
				dropdown: [],
				reference: 'Read more about the miminani project'
			},
			{
				caption: 'Github',
				icon: 'fa fa-github fa-lg',
				link: 'http://github.com/squarenomad/miminani',
				class: '',
				dropdown: [],
				reference: 'View our open source code'
			},
			{
				caption: 'Messages',
				icon: 'fa fa-inbox fa-lg',
				link: '#',
				class: '',
				dropdown: [],
				reference: 'Notifications and alerts'
			},
			{
				caption: 'User',
				icon: 'fa fa-user-circle fa-lg',
				link: '#',
				class: 'dropdown active',
				dropdown: [
					{
						caption:'Profile',
						link: '#',
						class: 'disabled'
					},
					{
						caption:'Settings',
						link: '#',
						class: 'disabled'
					},
					{
						caption:'Sign Out',
						link: '#',
						class: ''
					}
				],
				reference: 'Manage your profile'
			}
		],
		current_view: 'Relationships',
		panel_menus: [
			{
				panel: 'Relationships',
				reference: 'List all your relationships',
				icon: 'fa fa-users fa-lg',
				class: 'btn btn-lg btn-primary btn-block',
				length: 'col-md-4 col-sm-4 col-xs-4'
			},
			{
				panel: 'Relationships',
				reference: 'Add a relationship',
				icon: 'fa fa-user-plus fa-lg',
				class: 'btn btn-lg btn-info btn-block',
				length: 'col-md-4 col-sm-4 col-xs-4'
			},
			{
				panel: 'Relationships',
				reference: 'Edit a relationship',
				icon: 'fa fa-pencil-square fa-lg',
				class: 'btn btn-lg btn-warning btn-block',
				length: 'col-md-4 col-sm-4 col-xs-4'
			}
		]
	},
	computed: {
		receivedPanels: function() {
			for (i = 0; i < this.panel_menus.length; i++) {
				var items = [];
				items.push(this.panel_menus[i].panel)
				return items
			}
		}
	}
});