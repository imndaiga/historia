Vue.component('panel-navbar', {
	template: '#panel-navbar',
	props: {
		header: {
			type: String,
			required: true
		},
		menus: {
			type: Array,
			required: true
		}
	}
});

Vue.component('app-navbar', {
	template: '#app-navbar',
	props: {
		menu_state: {
			type: Object,
			required: true
		},
		open_submenu: {
			type: String,
			required: true
		}
	},
	data: function() {
		return {
			title: 'MIMINANI',
			menus: [
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
		}
	},
	methods: {
		maindropdown: function() {
			this.$emit('maindropdown')
		},
		subdropdown: function(menu) {
			this.$emit('subdropdown', menu)
		}
	}
});

Vue.component('app-sidebar', {
	template: "#app-sidebar",
	props: {
		start_panel: {
			type: String,
			required: true
		}
	},
	data: function() {
		return {
			panels: [
				'Overview',
				'Relationships',
				'Visualisation',
				'Share',
			],
			active_panel: this.start_panel[0].toUpperCase() + this.start_panel.replace('-panel','').slice(1)
		}
	},
	methods: {
		selected: function(panel) {
			this.active_panel = panel
			this.$emit('selected', panel)
		},
		isPanelCurrent: function(panel) {
			if (this.active_panel == panel) {
				return 'active'
			} else {
				return 'inactive'
			}
		}
	}
});

Vue.component('relationships-panel', {
	template: '#relationships-panel',
	data: function() {
		return {
			menus: [
				{
					name: 'List Relationships',
					reference: 'List all your relationships',
					icon: 'fa fa-users fa-lg',
					class: 'btn btn-lg btn-primary btn-block',
					length: 'col-md-4 col-sm-4 col-xs-4'
				},
				{
					name: 'Add Relationships',
					reference: 'Add a relationship',
					icon: 'fa fa-user-plus fa-lg',
					class: 'btn btn-lg btn-info btn-block',
					length: 'col-md-4 col-sm-4 col-xs-4'
				},
				{
					name: 'Edit Relationships',
					reference: 'Edit a relationship',
					icon: 'fa fa-pencil-square fa-lg',
					class: 'btn btn-lg btn-warning btn-block',
					length: 'col-md-4 col-sm-4 col-xs-4'
				}
			],
			header: 'Relationships',
			forms: [
				{
					parent_menu: 'Add Relationships',
					inputs: [
						{ placeholder: 'JohnOlooDoe@gmail.com', validate: "email" , name: 'Email'},
						{ placeholder: 'John', validate: "alpha" , name: 'First Name'},
						{ placeholder: 'Oloo', validate: "alpha" , name: 'Ethnic Name'},
						{ placeholder: 'Doe', validate: "alpha" , name: 'Last Name'}
					],
					submit: 'Add'
				}
			]
		}
	}
})

Vue.component('overview-panel', {
	template: '#overview-panel',
	data: function() {
		return {
			menus: [],
			header: 'Overview',
			forms: []
		}
	}
})

Vue.component('visualisation-panel', {
	template: '#visualisation-panel',
	data: function() {
		return {
			menus: [],
			header: 'Visualisation',
			forms: []
		}
	}
})

Vue.component('share-panel', {
	template: '#share-panel',
	data: function() {
		return {
			menus: [],
			header: 'Share',
			forms: []
		}
	}
})

Vue.use(VeeValidate);

var vm = new Vue({
	el: '#app',
	data: {
		current_view: 'relationships-panel',
		open_main_dropdown: false,
		open_sub_dropdown_name: ''
	},
	methods: {
		updateView: function(panel_name) {
			panel = panel_name.toLowerCase() + '-panel'
			this.current_view = panel
			this.open_main_dropdown = false
			this.open_sub_dropdown_name = ''
		},
		toggleMenu: function() {
			this.open_main_dropdown = !this.open_main_dropdown
			this.open_sub_dropdown_name = ''
		},
		toggleSubMenu: function(menu_name) {
			if (this.open_sub_dropdown_name == menu_name) {
				this.open_sub_dropdown_name = ''
			} else {
				this.open_sub_dropdown_name = menu_name
			}
		}
	}
});