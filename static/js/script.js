Vue.component('app-navbar', {
	template: '#app-navbar',
	props: {
		title: {
			type: String,
			required: true
		},
		nav_menus: {
			type: Array,
			required: true
		},

	},
	data: function() {
		return {
			open_main_dropdown: false,
			sub_menu_dropdown_name: ''
		}
	},
	methods: {
		toggleMainMenu: function() {
			this.open_main_dropdown = !this.open_main_dropdown
		},
		toggleSubMenu: function(submenu) {
			if (submenu == this.sub_menu_dropdown_name) {
				this.sub_menu_dropdown_name = ''
			} else {
				this.sub_menu_dropdown_name = submenu
			}
		},
		logout: function() {
			this.$parent.$parent.logout()
		},
		testSecured: function() {
			this.$parent.$parent.testSecured()
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
			type: Array,
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

Vue.component('multiselect', VueMultiselect.default)

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
			bus.$emit('alpha-changed', [field_name, value])
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
			bus.$emit('email-changed', [field_name, value])
		}
	}
})

Vue.component('pikaday-input', {
	template: '#pikaday-input',
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
	data: function() {
		return {
			picker: '',
			base_ref: this.input_name
		}
	},
	mounted: function() {
		this.picker = new Pikaday({
			ref: this.base_ref,
			field: this.$refs[this.base_ref],
			trigger: this.$refs[this.base_ref+'-btn'],
			onSelect: function() {
				date = this.getMoment().format('Do MMMM YYYY')
				bus.$emit('date-selected', [this._o.ref, date])
			}
		})
	}
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

Vue.component('multiselect-input', {
	template: '#multiselect-input',
	mixins: [window.VueMultiselect.multiselectMixin, window.VueMultiselect.pointerMixin],
	props: {
		label: {
			type: String,
			required: true
		},
		input_name: {
			type: String,
			required: true
		}
	},
	methods: {
		updateSelected: function(field_name, value) {
			bus.$emit('multi-selected', [field_name, value])
		}
	}
})

Vue.component('search-input', {
	template: '#search-input',
	mixins: [window.VueMultiselect.multiselectMixin, window.VueMultiselect.pointerMixin],
	props: {
		label: {
			type: String,
			required: true
		},
		input_name: {
			type: String,
			required: true
		}
	},
	data: function() {
		return {
			people: [],
			isLoading: false
		}
	},
	methods: {
		asyncFind: function(query) {
			this.isLoading = true
			console.log('Searching...')
			this.isLoading = false
		}
	}
})

const dashboard = Vue.component('dashboard-page', {
	template: '#dashboard-page',
	data: function() {
		return {
			current_panel_view: 'Add_Relationships',
			open_modal_state: false,
			open_modal_relationship_id: '',
			bs_panels: [
				{name: 'personal_details_panel', open: true, label: 'Personal Details'},
				{name: 'connect_relations_panel', open: false, label: 'Connect Relations'}],
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
							{type: 'alpha-input', first_name: '', placeholder: 'Enter First Name', input_name: 'add_first-name', label: 'First Name', bs_panel: 'personal_details_panel'},
							{type: 'alpha-input', ethnic_name: '', placeholder: 'Enter Ethnic Name', input_name: 'add_ethnic-name', label: 'Ethnic Name', bs_panel: 'personal_details_panel'},
							{type: 'alpha-input', last_name: '', placeholder: 'Enter Last Name', input_name: 'add_last-name', label: 'Last Name', bs_panel: 'personal_details_panel'},
							{type: 'email-input', email: '', placeholder: 'Enter Email Address', input_name: 'add_email', label: 'Email', bs_panel: 'personal_details_panel'},
							{type: 'search-input', relation: '', placeholder: 'Search for Relative', input_name: 'add_relation-person', label: 'Relative',
								multiselect_options: [],
								bs_panel: 'connect_relations_panel'
							},
							{type: 'multiselect-input', relation: '', placeholder: 'Choose a Relation', input_name: 'add_relation-name', label: 'Relation',
								multiselect_options: ['Father', 'Mother', 'Sister', 'Brother', 'Step-Father', 'Step-Mother', 'Step-Sister', 'Step-Brother'],
								bs_panel: 'connect_relations_panel'
							},
							{type: 'pikaday-input', birth_date: '', placeholder: 'Select Birth Date', input_name: 'add_birth-date', label: 'Date of Birth', bs_panel: 'personal_details_panel'}
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
								// birth_date:{value:'2017-02-15', type:'pikaday-input'}
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
					class: 'internal',
					dropdown: [],
					reference: 'Read more about the miminani project'
				},
				{
					caption: 'Github',
					icon: 'fa fa-github fa-lg',
					link: 'http://github.com/squarenomad/miminani',
					class: 'external',
					dropdown: [],
					reference: 'View our open source code'
				},
				{
					caption: 'Messages',
					icon: 'fa fa-inbox fa-lg',
					link: '#',
					class: 'internal',
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
							class: ''
						},
						{
							caption:'Sign Out',
							link: '#',
							class: 'logout'
						}
					],
					reference: 'Manage your profile'
				}
			]
		}
	},
	methods: {
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
				for (form_field in this.panel_views[this.current_Panel][this.current_panel_view].data) {
					if (Object.keys(this.panel_views[this.current_Panel][this.current_panel_view].data[form_field]).indexOf(field) != -1) {
						this.panel_views[this.current_Panel][this.current_panel_view].data[form_field][field] = value
					}
				}
			} else if (command == 'mod') {
				for (data_field in this.panel_views[this.current_Panel][this.current_panel_view].data) {
					for (model in this.panel_views[this.current_Panel][this.current_panel_view].data[data_field]) {
						if (model == 'id' && this.panel_views[this.current_Panel][this.current_panel_view].data[data_field][model].value == this.open_modal_relationship_id) {
							this.panel_views[this.current_Panel][this.current_panel_view].data[data_field][field].value = value
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
				if (Object.keys(this.panel_subnavs).indexOf(panel) != -1 && panel == this.current_Panel) {
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
		},
		current_Panel: function() {
			return this.$route.path.split('/')[2]
		}
	},
	created: function() {
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
			for (bs_panel_object in this.bs_panels) {
				if (this.bs_panels[bs_panel_object].name == bs_panel) {
					this.bs_panels[bs_panel_object].open = !this.bs_panels[bs_panel_object].open
				} else {
					this.bs_panels[bs_panel_object].open = false
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
		}.bind(this)),
		bus.$on('multi-selected', function(selection_data) {
			var command = selection_data[0].toString().split('_')[0]
			var field = selection_data[0].toString().split('_')[1]
			var value = selection_data[1]
			this.updateField(command, field, value)
		}.bind(this)),
		bus.$on('date-selected', function(selection_data) {
			var command = selection_data[0].toString().split('_')[0]
			var field = selection_data[0].toString().split('_')[1]
			var formatted_field = field.toString().replace('-','_')
			var value = selection_data[1]
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

const welcome = Vue.component('welcome-page', {
	template: '#welcome-page',
	data: function() {
		return {
			title: 'MIMINANI',
			nav_menus: [
				{
					caption: 'Info',
					icon: 'fa fa-info-circle fa-lg',
					link: '#',
					class: 'internal',
					dropdown: [],
					reference: 'Read more about the miminani project'
				},
				{
					caption: 'Github',
					icon: 'fa fa-github fa-lg',
					link: 'http://github.com/squarenomad/miminani',
					class: 'external',
					dropdown: [],
					reference: 'View our open source code'
				}
			],
			form: [
				{type: 'multiselect-input', residence: '', placeholder: 'Select Country', input_name: 'reg_residence', label: 'Country of Origin',
					multiselect_options: ['Kenya', 'Uganda', 'Tanzania']}
			],
			particlesjs_data : {
				"particles": {
				    "number": {"value": 80, "density": { "enable": true, "value_area": 800}},
				    "color": {"value": "#ffffff"},
				    "shape": {"type": "circle", "stroke": {"width": 0, "color": "#000000"},
					    "polygon": {"nb_sides": 5},
					    "image": {"src": "img/github.svg","width": 100,"height": 100}
					},
				    "opacity": {"value": 0.5,"random": false,
				    	"anim": {"enable": false,"speed": 1,"opacity_min": 0.1,"sync": false}
				    },
				    "size": {"value": 10,"random": true,
						"anim": {
							"enable": false,
							"speed": 80,
							"size_min": 0.1,
							"sync": false
						}
				    },
				    "line_linked": {"enable": true,"distance": 300,"color": "#ffffff","opacity": 0.4,"width": 2},
				    "move": {"enable": true,"speed": 3,"direction": "none","random": false,"straight": false,"out_mode": "out","bounce": false,
						"attract": {"enable": false,"rotateX": 600,"rotateY": 1200}
				    }
				  },
				"interactivity": {"detect_on": "canvas",
					"events": {
						"onhover": {"enable": false,"mode": "repulse"},
						"onclick": {"enable": true,"mode": "push"},
						"resize": true
					},
					"modes": {
						"grab": { "distance": 800,
							"line_linked": {"opacity": 1}
						},
						"bubble": {"distance": 800,"size": 80,"duration": 2,"opacity": 0.8,"speed": 3},
						"repulse": {"distance": 400,"duration": 0.4},
						"push": {"particles_nb": 4},
						"remove": {"particles_nb": 2}
					}
				},
				"retina_detect": true
			}
		}
	},
	computed: {
		authentication: function() {
			return this.$parent.authenticated
		}
	},
	mounted: function() {
		particlesJS('particlesjs', this.particlesjs_data)
	},
	methods: {
		login: function() {
			this.$parent.login()
		}
	}
})

const routes = [
	{ path: '/', component: welcome, beforeEnter: autoRoute},
	{ path: '/dashboard', component: dashboard, beforeEnter: requireAuth,
		children: [
			{path: 'Overview', component: dashboard, beforeEnter: requireAuth},
			{path: 'Relationships', component: dashboard, beforeEnter: requireAuth},
			{path: 'Visualisation', component: dashboard, beforeEnter: requireAuth},
			{path: 'Share', component: dashboard, beforeEnter: requireAuth},
			{path: '*', redirect: 'Overview', beforeEnter: requireAuth}
		]
	}
]

const router = new VueRouter({
	routes: routes
})

var bus = new Vue()

function checkAuth() {
	return !!localStorage.getItem('id_token')
}

function requireAuth(to, from, next) {
	if (!checkAuth()) {
		console.log('authorisation required')
		var path = '/'
		next({ path: path })
	} else {
		next()
	}
}

function autoRoute(to, from, next) {
	if (checkAuth()) {
		var path = '/dashboard/Overview'
		next({ path: path })
	} else {
		next()
	}
}

axios.interceptors.response.use(
function(response) {
	return response
},
function(error) {
	// Do something with response error
	if (error.response.status === 401) {
		console.log('unauthorized, logging out ...')
		localStorage.removeItem('id_token')
		localStorage.removeItem('profile')
		this.authenticated = false
		router.replace('/')
	}
	return Promise.reject(error)
})

var vm = new Vue({
	el: '#app',
	router: router,
	data: {
		authenticated: false,
		lock: new Auth0Lock('', '')
	},
	// Check the user's auth status when the app
	// loads to account for page refreshing
	mounted: function() {
		// set auth header on start up if token is present
		if (localStorage.getItem('id_token')) {
			axios.defaults.headers.common['Authorization'] = 'Bearer '+ localStorage.getItem('id_token')
		}
		axios.defaults.baseURL = ''
		var self = this
		this.authenticated = checkAuth()
		this.lock.on('authenticated', function(authResult) {
			console.log('authenticated')
			localStorage.setItem('id_token', authResult.idToken)
			self.lock.getUserInfo(authResult.accessToken, function(error, profile) {
				if (error) {
					// Handle error
					console.log('Error loading the Profile', error)
					return
				} else {
					// Set the token and user profile in local storage
					localStorage.setItem('profile', JSON.stringify(profile))
					self.authenticated = true
					axios.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('id_token')
					self.testSecured()
				}
			})
		})
		this.lock.on('authorization_error', function(error) {
			// handle error when authorizaton fails
		})
	},
	methods: {
		login: function() {
			this.lock.show()
		},
		logout: function() {
			localStorage.removeItem('id_token')
			localStorage.removeItem('profile')
			this.authenticated = false
			axios.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('id_token')
		},
		testSecured: function() {
			console.log('testing secured connection')
			axios.get('api/ping').then(
				function(response) {
					console.log(response)
				},
				function(response) {
					console.log(response)
				})
		}
	},
	watch: {
		authenticated: function(state) {
			// Automatically reload login page
			// when user logs out
			if (state == false) {
				router.push('/')
			}
		}
	}

})