Vue.component('app-panel', {
	template: '#app-panel'
});

Vue.component('app-navbar', {
	template: '#app-navbar',
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
		]
	}
});