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

Vue.component('panel-header', {
	template: '#panel-header',
	props: {
		current_panel: {
			type: String,
			required: true
		},
		subnav_dropdown: {
			type: Array,
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
		}
	}
})

Vue.component('panel-subnav', {
	template: '#panel-subnav',
	props: {
		subnav_menus: {
			type: Array,
			required: true
		},
		current_panel_view: {
			type: String,
			required: true
		}
	},
	methods: {
		panelViewSelected: function(panel_view) {
			bus.$emit('panel-view-selected', panel_view)
		}
	}
})

Vue.component('panel-form', {
	template: '#panel-form',
	props: {
		form : {
			type: Array,
			required: true
		},
		bs_panels: {
			type: Object,
			required: true
		}
	},
	methods: {
		bs_panel_selected: function(bs_panel) {
			bus.$emit('bs-panel-selected', bs_panel)
		}
	}
})

Vue.component('panel-table', {
	template: '#panel-table',
	props: {
		list: {
			type: Array,
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
		form: {
			type: Object,
			required: true
		}
	},
	methods: {
		closeModal: function() {
			bus.$emit('close-modal')
		}
	}
})

Vue.component('multiselect-input', VueMultiselect.default)

Vue.component('alpha-input', {
	template: '#alpha-input',
	props: {
		placeholder: {
			type: String,
			required: true
		},
		input_name: {
			type: String,
			required: true
		},
		label: {
			type: String,
			required: true
		}
	},
	methods: {
		alphaChanged: function(field_name, value) {
			bus.$emit('alpha-changed', [field_name, event.target.value])
		}
	}
})

Vue.component('email-input', {
	template: '#email-input',
	props: {
		placeholder: {
			type: String,
			required: true
		},
		input_name: {
			type: String,
			required: true
		},
		label: {
			type: String,
			required: true
		}
	},
	methods: {
		emailChanged: function(field_name, value) {
			bus.$emit('email-changed', [field_name, event.target.value])
		}
	}
})

Vue.component('pikaday-input', {
	template: '#pikaday-input'
})

Vue.component('hidden-input', {
	template: '#hidden-input',
	props: {
		input_name: {
			type: String,
			required: true
		},
		placeholder: {
			type: Number,
			required: true
		},
		label: {
			type: String,
			required: true
		}
	}
})

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
		bs_panels: { personal_details_panel: false, connect_relations_panel: true },
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
						{type: 'alpha-input', first_name: '', placeholder: 'Enter First Name', input_name: 'add_first-name', label: 'First Name'},
						{type: 'alpha-input', ethnic_name: '', placeholder: 'Enter Ethnic Name', input_name: 'add_ethnic-name', label: 'Ethnic Name'},
						{type: 'alpha-input', last_name: '', placeholder: 'Enter Last Name', input_name: 'add_last-name', label: 'Last Name'},
						{type: 'email-input', email: '', placeholder: 'Enter Email Address', input_name: 'add_email', label: 'Email'},
						{type: 'multiselect-input', relation: '', placeholder: 'Choose Relation', label: 'Relation',
							multiselect_options: ['Father', 'Mother', 'Sister', 'Brother', 'Step-Father', 'Step-Mother', 'Step-Sister', 'Step-Brother']
						},
						// {type: 'pikaday-input', birth_date: ''}
					]
				},
				List_Relationships: {
					type: 'Table',
					data: [
						{
							id:{value:1, type:'hidden-input', input_name: 'data_id', label: 'ID'},
							first_name:{value:'John', type:'alpha-input', input_name: 'mod_first-name', label: 'First Name'},
							ethnic_name:{value:'Mwaura', type:'alpha-input', input_name: 'mod_ethnic-name', label: 'Ethnic Name'},
							last_name:{value:'Ndungu', type:'alpha-input', input_name: 'mod_last-name', label: 'Last Name'},
							email:{value:'john.mwaura@gmail.com', type:'email-input', input_name: 'mod_email', label: 'Email'},
							// relation_name:{value:'Father', type:'multiselect-input'},
							// birth_date:{value:'2017-02-15', type:'pikaday-input'}
						},{
							id:{value:2, type:'hidden-input', input_name: 'data_id', label: 'ID'},
							first_name:{value:'Jane', type:'alpha-input', input_name: 'mod_first-name', label: 'First Name'},
							ethnic_name:{value:'Moraa', type:'alpha-input', input_name: 'mod_ethnic-name', label: 'Ethnic Name'},
							last_name:{value:'Ndungu', type:'alpha-input', input_name: 'mod_last-name', label: 'Last Name'},
							email:{value:'jane.mwaura@gmail.com', type:'email-input', input_name: 'mod_email', label: 'Email'},
							// relation_name:{value:'Mother', type:'multiselect-input'},
							// birth_date:{value:'2017-02-15', type:'pikaday-input'}
						},{
							id:{value:3, type:'hidden-input', input_name: 'data_id', label: 'ID'},
							first_name:{value:'Jack', type:'alpha-input', input_name: 'mod_first-name', label: 'First Name'},
							ethnic_name:{value:'Mutuku', type:'alpha-input', input_name: 'mod_ethnic-name', label: 'Ethnic Name'},
							last_name:{value:'Ndungu', type:'alpha-input', input_name: 'mod_last-name', label: 'Last Name'},
							email:{value:'jack.ndungu@gmail.com', type:'email-input', input_name: 'mod_email', label: 'Email'},
							// relation_name:{value:'Brother', type:'multiselect-input'},
							// birth_date:{value:'2017-02-15', type:'pikaday-input'}}
						}
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
		getViewData: function(panel_view) {
			for (iter_panel in this.panel_views) {
				for (view in this.panel_views[iter_panel]) {
					if (view == panel_view) {
						return this.panel_views[iter_panel][panel_view].data
					}
				}
			}
		},
		updateField: function(command, field, value) {
			if (command == 'add') {
				for (form_field in this.panel_views[this.current_panel][this.current_panel_view].data) {
					if (Object.keys(this.panel_views[this.current_panel][this.current_panel_view].data[form_field]).indexOf(field) != -1) {
						this.panel_views[this.current_panel][this.current_panel_view].data[form_field][field] = value
					}
				}
			} else if (command == 'mod') {
				for (data_field in this.panel_views[this.current_panel][this.current_panel_view].data) {
					for (model in this.panel_views[this.current_panel][this.current_panel_view].data[data_field]) {
						if (model == 'id' && this.panel_views[this.current_panel][this.current_panel_view].data[data_field][model].value == this.open_modal_relationship_id) {
							this.panel_views[this.current_panel][this.current_panel_view].data[data_field][field].value = value
						}
					}
				}
			}
		}
	},
	computed: {
		current_Subnavs: function() {
			for (index in this.all_panels) {
				panel = this.all_panels[index]
				if (Object.keys(this.panel_subnavs).indexOf(panel) != -1 && panel == this.current_panel) {
					return this.panel_subnavs[panel].navs
				}
			}
			return null
		},
		modal_Form: function() {
			data = this.getViewData(this.current_panel_view)
			for (i=0; i<data.length; i++) {
				if (data[i].id.value == this.open_modal_relationship_id) {
					return data[i]
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
							if (this.panel_views[panel][view].data[i].id.value == relationship_id) {
								this.panel_views[panel][view].data.splice(i, 1)
							}
						}
					}
				}
			}
		}.bind(this)),
		bus.$on('bs-panel-selected', function(bs_panel) {
			for (key in this.bs_panels) {
				if (key == bs_panel) {
					this.bs_panels[bs_panel] = !this.bs_panels[bs_panel]
				} else {
					this.bs_panels[key] = false
				}

			}
		}.bind(this)),
		bus.$on('alpha-changed', function(form_data) {
			var command = form_data[0].toString().split('_')[0]
			var field = form_data[0].toString().split('_')[1]
			var formatted_field = field.toString().replace('-','_')
			var value = form_data[1]
			this.updateField(command, formatted_field, value)
		}.bind(this)),
		bus.$on('email-changed', function(form_data) {
			var command = form_data[0].toString().split('_')[0]
			var field = form_data[0].toString().split('_')[1]
			var formatted_field = field.toString().replace('-','_')
			var value = form_data[1]
			this.updateField(command, formatted_field, value)
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
			} else {
				value = value.toString()
				return value.charAt(0).toUpperCase() + value.slice(1)
			}
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
			} else {
				value = value.toString()
				return value.replace('_',' ')
			}
		}
	}
})