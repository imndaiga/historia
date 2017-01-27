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
				dropdown: []
			},
			{
				caption: 'Github',
				icon: 'fa fa-github fa-lg',
				link: 'http://github.com/squarenomad/miminani',
				class: '',
				dropdown: []
			},
			{
				caption: 'Messages',
				icon: 'fa fa-inbox fa-lg',
				link: '#',
				class: '',
				dropdown: []
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
				]
			}
		],
		current_view: 'Overview',
		panel_menus: [
			{
				panel: 'Relationships',
				caption: 'List',
				icon: 'fa fa-users fa-lg',
				class: 'btn btn-lg btn-primary btn-block',
				length: 'col-md-4 col-sm-4 col-xs-4'
			},
			{
				panel: 'Relationships',
				caption: 'Add',
				icon: 'fa fa-user-plus fa-lg',
				class: 'btn btn-lg btn-info btn-block',
				length: 'col-md-4 col-sm-4 col-xs-4'
			},
			{
				panel: 'Relationships',
				caption: 'Edit',
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