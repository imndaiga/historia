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
			type: Object,
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
		schema: {
			type: Object,
			required: true
		},
		model: {
			type: Object,
			required: true
		},
		options: {
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

Vue.component('multiselect', VueMultiselect.default)

Vue.use(VueFormGenerator)

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
		bs_panels: {
			personal_details_panel: false,
			connect_relations_panel: true
		},
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
					data: {
						model: {
							fname: '',
							ename: '',
							lname: '',
							relation: '',
							email: '',
							bdate: ''
						},
						schema: {
							fields: [
								{
									type: 'input',
									inputType: 'text',
									label: 'First name',
									model: 'fname',
									placeholder: 'John',
									required: true,
									validator: VueFormGenerator.validators.alpha
								},{
									type: 'input',
									inputType: 'text',
									label: 'Ethnic name',
									model: 'ename',
									placeholder: 'Mutuku',
									required: true,
									validator: VueFormGenerator.validators.alpha
								},{
									type: 'input',
									inputType: 'text',
									label: 'Last name',
									model: 'lname',
									placeholder: 'Mbuvi',
									required: true,
									validator: VueFormGenerator.validators.alpha
								},{
									type: 'vueMultiSelect',
									label: 'Relation',
									model: 'relation',
									multiSelect: false,
									values: ['Father','Mother', 'Brother', 'Sister', 'Step-Mother',
											'Step-Father', 'Step-Brother', 'Step-Sister']
								},{
									type: 'input',
									inputType: 'email',
									label: 'E-mail',
									model: 'email',
									placeholder: "John.Mbuvi@gmail.com",
									validator: VueFormGenerator.validators.email
								},{
									type: 'input',
									inputType: 'text',
									label: 'Birthday',
									model: 'birth_date',
									placeholder: 'Select Birth Date',
									readonly: true,
									inputName: 'birth_date',
									buttons: [
										{
											classes: 'calendar-button',
											label: ' ',
											onclick: function() {
												var picker = new Pikaday ({
													field: document.getElementsByName('birth_date')[0],
													trigger: document.getElementsByClassName('calendar-button')[0],
													onClose: function() {
														bus.$emit('destroy-picker', this)
													}
												})
												bus.$emit('open-picker', picker)
											}
										}
									],
									validator: VueFormGenerator.validators.date
								}
							]
						},
						formOptions: {
							validateAfterLoad: false,
							validateAfterChanged: true
						}
					}
				},
				List_Relationships: {
					type: 'Table',
					data: [
						{id:'1', first_name: 'John', ethnic_name: 'Mwaura', last_name: 'Ndungu', relation_name: 'Father', email: 'john.mwaura@gmail.com', birth_date: '2017-02-15'},
						{id:'2', first_name: 'Jane', ethnic_name: 'Moraa', last_name: 'Ndungu', relation_name: 'Mother', email: 'jane.mwaura@gmail.com', birth_date: '2017-02-15'},
						{id:'3', first_name: 'Jack', ethnic_name: 'Mutuku', last_name: 'Ndungu', relation_name: 'Brother', email: 'jack.ndungu@gmail.com', birth_date: '2017-02-15'}
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
		],
		modal_schema: {
			fields: [
				{
					type: 'input',
					inputType: 'text',
					label: 'First name',
					model: 'first_name',
					inputName: 'first_name',
					placeholder: 'John',
					styleClasses: 'readonly-input',
					validator: VueFormGenerator.validators.alpha,
					buttons: [
						{
							label: 'Change',
							onclick: function() {
								document.getElementsByName('first_name')[0].parentElement.parentElement.parentElement.classList.remove('readonly-input')
							}
						}
					]
				},{
					type: 'input',
					inputType: 'text',
					label: 'Ethnic name',
					model: 'ethnic_name',
					inputName: 'ethnic_name',
					placeholder: 'Mutuku',
					styleClasses: 'readonly-input',
					validator: VueFormGenerator.validators.alpha,
					buttons: [
						{
							label: 'Change',
							onclick: function() {
								document.getElementsByName('ethnic_name')[0].parentElement.parentElement.parentElement.classList.remove('readonly-input')
							}
						}
					]
				},{
					type: 'input',
					inputType: 'text',
					label: 'Last name',
					model: 'last_name',
					inputName: 'last_name',
					placeholder: 'Mbuvi',
					styleClasses: 'readonly-input',
					validator: VueFormGenerator.validators.alpha,
					buttons: [
						{
							label: 'Change',
							onclick: function() {
								document.getElementsByName('last_name')[0].parentElement.parentElement.parentElement.classList.remove('readonly-input')
							}
						}
					]
				},{
					type: 'vueMultiSelect',
					label: 'Relation',
					model: 'relation_name',
					inputName: 'relation_name',
					multiSelect: false,
					styleClasses: 'disable-multiselect',
					values: ['Father','Mother', 'Brother', 'Sister', 'Step-Mother',
							'Step-Father', 'Step-Brother', 'Step-Sister'],
					buttons: [
						{
							classes: 'button-active',
							label: 'Change',
							onclick: function() {
								document.getElementsByClassName('field-vueMultiSelect')[0].classList.remove('disable-multiselect')
							}
						}
					]
				},{
					type: 'input',
					inputType: 'email',
					label: 'E-mail',
					model: 'email',
					inputName: 'email',
					placeholder: "John.Mbuvi@gmail.com",
					styleClasses: 'readonly-input',
					validator: VueFormGenerator.validators.email,
					buttons: [
						{
							label: 'Change',
							onclick: function() {
								document.getElementsByName('email')[0].parentElement.parentElement.parentElement.classList.remove('readonly-input')
							}
						}
					]
				},{
					type: 'input',
					inputType: 'text',
					label: 'Date of Birth',
					placeholder: 'Select Calendar Date',
					model: 'birth_date',
					inputName: 'birth_date',
					readonly: true,
					styleClasses: 'disable-buttons',
					validator: VueFormGenerator.validators.date,
					pikadayOptions: {
						position: "top right"
					},
					buttons: [
						{
							classes: 'calendar-button button-disabled',
							label: ' ',
							onclick: function() {
								var picker = new Pikaday ({
									field: document.getElementsByName('birth_date')[0],
									trigger: document.getElementsByClassName('calendar-button')[0],
									onClose: function() {
										bus.$emit('destroy-picker', this)
									}
								})
								bus.$emit('open-picker', picker)
							}
						},{
							classes: 'button-active',
							label: 'Change',
							onclick: function() {
								document.getElementsByClassName('calendar-button')[0].classList.remove('button-disabled')
							}
						}
					]
				}
			]
		},
		modal_options: {
			validateAfterLoad: false,
			validateAfterChanged: true
		}
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
		getPanelViewObject: function(panel, panel_view) {
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
		getViewData: function(panel_view) {
			for (iter_panel in this.panel_views) {
				for (view in this.panel_views[iter_panel]) {
					if (view == panel_view) {
						return this.panel_views[iter_panel][panel_view].data
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
		modal_Model: function() {
			data = this.getViewData(this.current_panel_view)
			for (relation in data) {
				if (data[relation].id == this.open_modal_relationship_id) {
					var model = data[relation]
				}
			}
			return model
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
		}.bind(this)),
		bus.$on('open-picker', function(picker) {
			picker.show()
		}),
		bus.$on('destroy-picker', function(picker) {
			picker.destroy()
		}),
		bus.$on('bs-panel-selected', function(bs_panel) {
			for (key in this.bs_panels) {
				if (key == bs_panel) {
					this.bs_panels[bs_panel] = !this.bs_panels[bs_panel]
				} else {
					this.bs_panels[key] = false
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