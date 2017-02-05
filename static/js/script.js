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

Vue.component('panel-subnav', {
	template: '#panel-subnav',
	props: {
		current_panel: {
			type: String,
			required: true
		},
		subnav_menus: {
			type: Array,
			required: true
		},
		subnav_dropdown: {
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

Vue.component('panel-form', {
	template: '#panel-form',
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

Vue.component('panel-table', {
	template: '#panel-table',
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
		current_panel: 'Relationships',
		current_panel_view: 'Add_Relationships',
		open_main_dropdown: false,
		open_sub_dropdown_name: '',
		open_modal_state: false,
		open_modal_relationship_id: '',
		all_panels : ['Overview', 'Relationships', 'Visualisation', 'Share'],
		panel_subnavs : {
			Relationships: {
				navs: [
					{
						title: 'List_Relationships',
						info: 'List all your relationships',
						fa_icon: 'fa fa-users fa-lg',
						bs_button: 'btn btn-lg btn-primary btn-block',
						bs_grid_length: 'col-md-6 col-sm-6 col-xs-6',
					},{
						title: 'Add_Relationships',
						info: 'Add a relationship to your tree',
						fa_icon: 'fa fa-user-plus fa-lg',
						bs_button: 'btn btn-lg btn-info btn-block',
						bs_grid_length: 'col-md-6 col-sm-6 col-xs-6',
					}
				]
			}
		},
		panel_views : {
			Relationships: {
				Add_Relationships: {
					type: 'Form',
					data: [
						{ placeholder: 'JohnOlooDoe@gmail.com', validate: "email" , name: 'Email', type: 'email'},
						{ placeholder: 'John', validate: "required|alpha" , name: 'First Name', type: 'alpha'},
						{ placeholder: 'Oloo', validate: "required|alpha" , name: 'Ethnic Name', type: 'alpha'},
						{ placeholder: 'Doe', validate: "required|alpha" , name: 'Last Name', type: 'alpha'},
						{ placeholder: 'Father', validate: "required|alpha" , name: 'Relationship Name', type: 'alpha'}
					]
				},
				List_Relationships: {
					type: 'Table',
					data: [
						{id:'1', first_name: 'John', baptism_name: 'Charles', ethnic_name: 'Mwaura', last_name: 'Ndungu', relation_name: 'Father'},
						{id:'2', first_name: 'Jane', baptism_name: 'Christine', ethnic_name: 'Moraa', last_name: 'Ndungu', relation_name: 'Mother'},
						{id:'3', first_name: 'Jack', baptism_name: 'Christian', ethnic_name: 'Mutuku', last_name: 'Ndungu', relation_name: 'Brother'}
					]
				}

			}
		},
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
		isNavigationAllowed: function(panel, panel_view, view_type) {
			for (index in this.all_panels) {
				iter_panel = this.all_panels[index]
				if (iter_panel == panel) {
					for (view in this.panel_views[panel]) {
						if (view == panel_view) {
							if (this.panel_views[panel][view].type == view_type) {
								return true
							}
						}
					}
				}
			}
			return false
		},
		getPanelViewData: function(panel, panel_view) {
			for (iter_panel in this.panel_views) {
				if (iter_panel == panel) {
					for (view in this.panel_views[panel]) {
						if (view == panel_view) {
							return this.panel_views[panel][view]
						}
					}
				}
			}
			return null
		},
		getViewFields: function(panel_view, exceptions=[]) {
			fields = []
			for (panel in this.panel_views) {
				for (view in this.panel_views[panel]) {
					if (view == panel_view) {
						for (entry in this.panel_views[panel][view].data) {
							for (field in this.panel_views[panel][view].data[entry]) {
								if (fields.indexOf(field) == -1 && exceptions.indexOf(field) == -1) {
									fields.push(field)
								}
							}
						}
					}
				}
			}
			return fields
		},
		getViewFieldData: function(panel_view) {
			for (iter_panel in this.panel_views) {
				for (view in this.panel_views[iter_panel]) {
					if (view == panel_view) {
						return this.panel_views[iter_panel][panel_view].data
					}
				}
			}
		},
		getModalRelationshipData: function(panel_view) {
			data = this.getViewFieldData(panel_view)
			for (relation in data) {
				if (data[relation].id == this.open_modal_relationship_id) {
					return data[relation]
				}
			}
		}
	},
	computed: {
		currentSubnavs: function() {
			for (index in this.all_panels) {
				panel = this.all_panels[index]
				if (Object.keys(this.panel_subnavs).indexOf(panel) != -1 && panel == this.current_panel) {
					return this.panel_subnavs[panel].navs
				}
			}
			return null
		}
	},
	created: function() {
		bus.$on('panel-selected', function(panel) {
			this.current_panel = panel
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
			for (panel in this.panel_views) {
				for (view in this.panel_views[panel]) {
					if (view == 'List_Relationships') {
						for (i=0; i<this.panel_views[panel][view].data.length; i++) {
							if (this.panel_views[panel][view].data[i].id == relationship_id) {
								this.panel_views[panel][view].data.splice(i, 1)
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