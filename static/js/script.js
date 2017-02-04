Vue.component('panel-navbar', {
	template: '#panel-navbar',
	props: {
		current_panel: {
			type: String,
			required: true
		},
		button_menus: {
			type: Array,
			required: true
		},
		dropdown_menu: {
			type: Array,
			required: true
		},
		current_panel_view: {
			type: String,
			required: true
		}
	},
	data: function() {
		return {
			open_panel_menu: false
		}
	},
	methods: {
		togglePanelMenu: function() {
			this.open_panel_menu = !this.open_panel_menu
		},
		panelSelected: function(panel) {
			this.open_panel_menu = false
			bus.$emit('panel-selected', panel)
		},
		panelViewSelected: function(panel_view) {
			this.open_panel_menu = false
			bus.$emit('panel-view-selected', panel_view)
		}
	}
})

Vue.component('app-navbar', {
	template: '#app-navbar',
	props: {
		nav_state: {
			type: Object,
			required: true
		},
		open_submenu: {
			type: String,
			required: true
		},
		title: {
			type: String,
			required: true
		},
		nav_menus: {
			type: Array,
			required: true
		},

	},
	methods: {
		maindropdown: function() {
			this.$emit('maindropdown')
		},
		subdropdown: function(menu) {
			this.$emit('subdropdown', menu)
		}
	}
})

Vue.component('app-sidebar', {
	template: "#app-sidebar",
	props: {
		current_panel: {
			type: String,
			required: true
		},
		panels: {
			type: Array,
			required: true
		}
	},
	methods: {
		panelSelected: function(panel) {
			bus.$emit('panel-selected', panel)
		}
	}
})

Vue.component('form-pane', {
	template: '#form-pane',
	props: {
		form : {
			type: Object,
			required: true
		}
	},
	methods: {
		validateAll: function() {
			this.$validator.validateAll().then(function(result) {
				alert('Form Submitted')
			}).catch(function(failure) {
				alert('Please correct form details')
			})
		}
	}
})

Vue.component('table-pane', {
	template: '#table-pane',
	props: {
		list: {
			type: Object,
			required: true
		},
		table_headers: {
			type: Array,
			required: true
		}
	},
	methods: {
		openRelation: function(relation_id) {
			bus.$emit('open-relation-modal', relation_id)
		},
		deleteRelation: function(relation_id) {
			bus.$emit('delete-relation', relation_id)
		}
	}
})

Vue.component('modal-window', {
	template: '#modal-window',
	props: {
		relationship_data: {
			type: Object,
			required: true
		},
		form_labels: {
			type: Array,
			required: true
		}
	},
	data: function() {
		return {
			active_form_fields : []
		}
	},
	methods: {
		closeModal: function() {
			bus.$emit('close-modal')
		},
		activateFormField: function(form_field) {
			this.active_form_fields.push(form_field)
		}
	}
})

Vue.use(VeeValidate);

var bus = new Vue()

var vm = new Vue({
	el: '#app',
	data: {
		current_view: 'Relationships',
		current_panel_view: 'List Relationships',
		open_main_dropdown: false,
		open_sub_dropdown_name: '',
		open_modal_state: false,
		open_modal_relationship_id: '',
		panels: [
			{
				name: 'Overview',
				menus: [],
				views: []
			},{
				name: 'Relationships',
				menus: [
					{
						name: 'List Relationships',
						reference: 'List all your relationships',
						icon: 'fa fa-users fa-lg',
						class: 'btn btn-lg btn-primary btn-block',
						length: 'col-md-6 col-sm-6 col-xs-6'
					},
					{
						name: 'Add Relationships',
						reference: 'Add a relationship',
						icon: 'fa fa-user-plus fa-lg',
						class: 'btn btn-lg btn-info btn-block',
						length: 'col-md-6 col-sm-6 col-xs-6'
					}
				],
				views: [
					{
						type: 'Form',
						name: 'Add Relationships',
						inputs: [
							{ placeholder: 'JohnOlooDoe@gmail.com', validate: "email" , name: 'Email', type: 'email'},
							{ placeholder: 'John', validate: "required|alpha" , name: 'First Name', type: 'alpha'},
							{ placeholder: 'Oloo', validate: "required|alpha" , name: 'Ethnic Name', type: 'alpha'},
							{ placeholder: 'Doe', validate: "required|alpha" , name: 'Last Name', type: 'alpha'},
							{ placeholder: 'Father', validate: "required|alpha" , name: 'Relationship Name', type: 'alpha'}
						],
						submit: 'Add'
					},
					{
						type: 'Table',
						name: 'List Relationships',
						data: [
							{id:'1', first_name: 'John', baptism_name: 'Charles', ethnic_name: 'Mwaura', last_name: 'Ndungu', relation_name: 'Father'},
							{id:'2', first_name: 'Jane', baptism_name: 'Christine', ethnic_name: 'Moraa', last_name: 'Ndungu', relation_name: 'Mother'},
							{id:'3', first_name: 'Jack', baptism_name: 'Christian', ethnic_name: 'Mutuku', last_name: 'Ndungu', relation_name: 'Brother'},
						]
					}
				]
			},{
				name: 'Visualisation',
				menus: [],
				views: []
			},{
				name: 'Share',
				menus: [],
				views: []
			}
		],
		title: 'MIMINANI',
		nav_menus: [
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
		]
	},
	methods: {
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
		},
		navigateAllowed: function(current_view, current_panel_view, view_type_list) {
			if (view_type_list.indexOf(current_panel_view) != -1) {
				for (i=0; i<this.panels.length; i++) {
					if (this.panels[i].name == current_view) {
						for (j=0; j<this.panels[i].views.length; j++) {
							if (this.panels[i].views[j].name == current_panel_view) {
								return true
							}
						}
						return false
					}
				}
			}
			return false
		},
		getPanelView: function(current_panel_view) {
			for (i=0; i < this.panels.length; i++) {
				if (this.panels[i].name == this.current_view) {
					for (j=0; j<this.panels[i].views.length; j++) {
						if (this.panels[i].views[j].name == current_panel_view) {
							return this.panels[i].views[j]
						}
					}
				}
			}
		},
		getTableHeaders: function(current_panel_view) {
			headers = []
			for (i=0; i < this.panels.length; i++) {
				if (this.panels[i].name == this.current_view) {
					for (j=0; j<this.panels[i].views.length; j++) {
						if (this.panels[i].views[j].name == current_panel_view) {
							if (this.panels[i].views[j].type == 'Table') {
								for (k=0; k<this.panels[i].views[j].data.length; k++) {
									row_headers = Object.keys(this.panels[i].views[j].data[k])
									for (l=0; l<row_headers.length; l++) {
										if (headers.indexOf(row_headers[l]) == -1 && row_headers[l] != 'id') {
											headers.push(row_headers[l])
										}
									}
								}
							}
						}
					}
				}
			}
			return headers
		}
	},
	computed: {
		allPanelNames: function() {
			panel_names_array = []
			for (i = 0; i < this.panels.length; i++) {
				panel_names_array.push(this.panels[i].name)
			}
			return panel_names_array
		},
		currentPanelMenus: function() {
			for (i = 0; i < this.panels.length; i++) {
				if (this.panels[i].name == this.current_view) {
					return this.panels[i].menus
				}
			}
		},
		formViews: function() {
			view_type_list = []
			for (i=0; i < this.panels.length; i++) {
				if (this.panels[i].name == this.current_view) {
					for (j=0; j<this.panels[i].views.length; j++) {
						if (this.panels[i].views[j].type == 'Form') {
							view_type_list.push(this.panels[i].views[j].name)
						}
					}
				}
			}
			return view_type_list
		},
		tableViews: function() {
			view_type_list = []
			for (i=0; i < this.panels.length; i++) {
				if (this.panels[i].name == this.current_view) {
					for (j=0; j<this.panels[i].views.length; j++) {
						if (this.panels[i].views[j].type == 'Table') {
							view_type_list.push(this.panels[i].views[j].name)
						}
					}
				}
			}
			return view_type_list
		},
		relationshipData: function() {
			for (i=0; i < this.panels.length; i++) {
				if (this.panels[i].name == this.current_view) {
					for (j=0; j<this.panels[i].views.length; j++) {
						if (this.panels[i].views[j].type == 'Table') {
							for (k=0; k<this.panels[i].views[j].data.length; k++) {
								if (this.panels[i].views[j].data[k].id == this.open_modal_relationship_id) {
									return this.panels[i].views[j].data[k]
								}
							}
						}
					}
				}
			}
		}
	},
	created: function() {
		bus.$on('panel-selected', function(panel) {
			this.current_view = panel
			this.open_main_dropdown = false
			this.open_sub_dropdown_name = ''
		}.bind(this)),
		bus.$on('panel-view-selected', function(panel_view) {
			this.open_main_dropdown = false
			this.current_panel_view = panel_view
		}.bind(this)),
		bus.$on('open-relation-modal', function(relationship_id) {
			this.open_main_dropdown = false
			this.open_modal_state = true
			this.open_modal_relationship_id = relationship_id
		}.bind(this)),
		bus.$on('close-modal', function() {
			this.open_modal_state = false
			this.open_modal_relationship_id = ''
		}.bind(this)),
		bus.$on('delete-relation', function(relationship_id) {
			for (i=0; i < this.panels.length; i++) {
				if (this.panels[i].name == this.current_view) {
					for (j=0; j<this.panels[i].views.length; j++) {
						if (this.panels[i].views[j].type == 'Table') {
							for (k=0; k<this.panels[i].views[j].data.length; k++) {
								if (this.panels[i].views[j].data[k].id == relationship_id) {
									// invoke API DELETE method to remove from database
									this.panels[i].views[j].data.splice(k,1)
								}
							}
						}
					}
				}
			}
		}.bind(this))
	},
	filters: {
		capitalize : function(value) {
			if (!value) return ''
			if (typeof value == "object") {
				cap_array = []
				for (i=0; i<value.length; i++) {
					new_value = value[i].charAt(0).toUpperCase() + value[i].slice(1)
					cap_array.push(new_value)
				}
			return cap_array
			}
			value = value.toString()
			return value.charAt(0).toUpperCase() + value.slice(1)
		},
		spacereplace: function(value) {
			if (!value) return ''
			if (typeof value == "object") {
				spaced_array = []
				for (i=0; i<value.length; i++) {
					new_value = value[i].toString().replace('_',' ')
					spaced_array.push(new_value)
				}
			return spaced_array
			}
			value = value.toString()
			return value.charAt(0).toUpperCase() + value.slice(1)
		}
	}
})