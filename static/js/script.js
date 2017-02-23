// Create axios instance
var HTTP = axios.create({
	baseURL: ''
})

// Set up axios interceptors to error responses
HTTP.interceptors.response.use(
function(response) {
	return response
},
function(error) {
	// Do something with response error
	if (error.response.status === 401) {
		error_obj = {'error_message': [{
			'code': error.response.data.code,
			'description': error.response.data.description
		}]}
		console.log('unauthorized, logging out ...')
		console.log(error_obj)
		localStorage.removeItem('id_token')
		localStorage.removeItem('profile')
		this.authenticated = false
		router.replace('/')
	}
	return Promise.reject(error)
})

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
		panels: {
			type: Array,
			required: true
		}
	},
	methods: {
		panelViewSelected: function(panel_view) {
			bus.$emit('panel-view-selected', panel_view)
		}
	},
	computed: {
		current_Panel: function() {
			return this.$route.path.split('/')[2].charAt(0).toUpperCase() + this.$route.path.split('/')[2].slice(1)
		}
	}
})

Vue.component('panel-header', {
	template: '#panel-header',
	props: {
		panels: {
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
	},
	computed: {
		current_Panel: function() {
			return this.$route.path.split('/')[2].charAt(0).toUpperCase() + this.$route.path.split('/')[2].slice(1)
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
	data: function() {
		return {
			updatedFields: {}
		}
	},
	methods: {
		bs_panel_selected: function(bs_panel) {
			bus.$emit('bs-panel-selected', bs_panel)
		},
		submitForm: function() {
			var self = this
			HTTP.put('/api/relationships', {
				data: JSON.stringify(this.updatedFields)
			}).then(
				function(response) {
					console.log(response)
				},
				function(response) {
					console.log(response)
				}
			)
		},
		updateField: function(command, input_name, value) {
			if (command == 'add') {
				for (index in this.form) {
					if (this.form[index].input_name == input_name) {
						field_name = input_name.split('_')[1].replace('-','_')
						if (this.form[index][field_name] != value) {
							this.updatedFields.task = command
							this.updatedFields[field_name] = value
						}
					}
				}
			} else if (command == 'mod') {
				// for (index in this.form) {
				// 	if (this.form[index].input_name == input_name) {
				// 		field_name = input_name.split('_')[1].replace('-','_')
				// 		if (this.form[index][field_name] != value) {
				// 			this.updatedFields.task = command
				// 			this.updatedFields[field_name] = value
				// 		}
				// 	}
				// }
			}
		}
	},
	created: function() {
		bus.$on('bs-panel-selected', function(bs_panel) {
			for (bs_panel_object in this.bs_panels) {
				if (this.bs_panels[bs_panel_object].name == bs_panel) {
					this.bs_panels[bs_panel_object].open = !this.bs_panels[bs_panel_object].open
				} else {
					this.bs_panels[bs_panel_object].open = false
				}

			}
		}.bind(this))
		bus.$on('alpha-changed', function(form_data) {
			var command = form_data[0].toString().split('_')[0]
			var input_name = form_data[0].toString()
			var value = form_data[1]
			this.updateField(command, input_name, value)
		}.bind(this))
		bus.$on('email-changed', function(form_data) {
			var command = form_data[0].toString().split('_')[0]
			var input_name = form_data[0].toString()
			var value = form_data[1]
			this.updateField(command, input_name, value)
		}.bind(this))
		bus.$on('multi-selected', function(selection_data) {
			var command = selection_data[0].toString().split('_')[0]
			var input_name = selection_data[0].toString()
			var value = selection_data[1]
			this.updateField(command, input_name, value)
		}.bind(this))
		bus.$on('date-selected', function(selection_data) {
			var command = selection_data[0].toString().split('_')[0]
			var input_name = selection_data[0].toString()
			var value = selection_data[1]
			this.updateField(command, input_name, value)
		}.bind(this))
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

Vue.component('submit-button', {
	template: '#submit-button',
	props: {
		button_class: {
			type: String,
			required: true
		},
		button_message: {
			type: String,
			required: true
		}
	}
})

const dashboard = Vue.component('dashboard-page', {
	template: '#dashboard-page',
	data: function() {
		return {
			panels : [
				{ name: 'Overview', navs: []},
				{ name: 'Visualisation', navs: []},
				{ name: 'Share', navs: []},
				{ name: 'Relationships',
					navs: [
						{
							title: 'List Relationships',
							info: 'List all your relationships',
							view: 'List_Relationships'
						},{
							title: 'Add Relationships',
							info: 'Add a relationship to your tree',
							view: 'Add_Relationships'
						}
					],
					default_view: 'List_Relationships'
				}
			],
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

const relationships = Vue.component('relationships-page', {
	template: '#relationships-page'
})

const add_relationships = Vue.component('add-relationships-page', {
	template: '#add-relationships-page',
	data: function() {
		return {
			bs_panels: [
				{name: 'personal_details_panel', open: false, label: 'Personal Details'},
				{name: 'connect_relations_panel', open: false, label: 'Connect Relations'}],
			form_data: [
				{type: 'alpha-input', first_name: '', placeholder: 'Enter First Name', input_name: 'add_first-name', label: 'First Name', bs_panel: 'personal_details_panel'},
				{type: 'alpha-input', ethnic_name: '', placeholder: 'Enter Ethnic Name', input_name: 'add_ethnic-name', label: 'Ethnic Name', bs_panel: 'personal_details_panel'},
				{type: 'alpha-input', last_name: '', placeholder: 'Enter Last Name', input_name: 'add_last-name', label: 'Last Name', bs_panel: 'personal_details_panel'},
				{type: 'email-input', email: '', placeholder: 'Enter Email Address', input_name: 'add_email', label: 'Email', bs_panel: 'personal_details_panel'},
				{type: 'search-input', relation_person: '', placeholder: 'Search for Relative', input_name: 'add_relation-person', label: 'Relative',
					multiselect_options: [],
					bs_panel: 'connect_relations_panel'
				},
				{type: 'multiselect-input', relation_name: '', placeholder: 'Choose a Relation', input_name: 'add_relation-name', label: 'Relation',
					multiselect_options: ['Father', 'Mother', 'Sister', 'Brother', 'Step-Father', 'Step-Mother', 'Step-Sister', 'Step-Brother'],
					bs_panel: 'connect_relations_panel'
				},
				{type: 'pikaday-input', birth_date: '', placeholder: 'Select Birth Date', input_name: 'add_birth-date', label: 'Date of Birth', bs_panel: 'personal_details_panel'},
				{type: 'submit-button', button_message: 'Save Details', button_name: 'add_personal-details', bs_panel: 'personal_details_panel', button_class: 'btn btn-lg btn-success btn-block'},
				{type: 'submit-button', button_message: 'Save Relation', button_name: 'add_connect-relations', bs_panel: 'connect_relations_panel', button_class: 'btn btn-lg btn-success btn-block'}

			]
		}
	}
})

const list_relationships = Vue.component('list-relationships-page', {
	template: '#list-relationships-page',
	data: function() {
		return {
			open_modal_state: false,
			open_modal_relationship_id: '',
			table_data: []
		}
	},
	methods: {
		fetchData: function() {
			var self = this
			HTTP.get('/api/relationships').then(
				function(response) {
					self.table_data = response.data
				},
				function(response) {
					console.log(response)
				}
			)
		}
	},
	computed: {
		modal_Form: function() {
			for (i=0; i<this.table_data.length; i++) {
				if (this.table_data[i].id.value == this.open_modal_relationship_id) {
					return this.table_data[i]
				}
			}
		},
		table_Headers: function() {
			headers = []
			for (entry in this.table_data) {
				for (field in this.table_data[entry]) {
					header = this.table_data[entry][field].label
					if (headers.indexOf(header) == -1 && header != 'ID') {
						headers.push(this.table_data[entry][field].label)
					}
				}
			}
			return headers
		}
	},
	mounted: function() {
		this.fetchData()
	},
	created: function() {
		bus.$on('open-relation-modal', function(relationship_id) {
			this.open_modal_state = true
			this.open_modal_relationship_id = relationship_id
		}.bind(this))
		bus.$on('close-modal', function() {
			this.open_modal_state = false
			this.open_modal_relationship_id = ''
		}.bind(this))
		bus.$on('delete-relation', function(relationship_id) {
			var self = this
			HTTP.delete('/api/relationships', {
				data: relationship_id
			}).then(
				function(response) {
					console.log('record deleted')
					self.table_data = response.data
				},
				function(response) {
					console.log(response)
				}
			)
		}.bind(this))
	}
})

const visualisation = Vue.component('visualisation-page', {
	template: '#visualisation-page'
})

const share = Vue.component('share-page', {
	template: '#share-page'
})

const overview = Vue.component('overview-page', {
	template: '#overview-page'
})

const routes = [
	{ path: '/', component: welcome, beforeEnter: autoRoute},
	{ path: '/dashboard', component: dashboard, beforeEnter: requireAuth,
		children: [
			{path: 'overview', name: 'Overview', component: overview, beforeEnter: requireAuth},
			{path: 'relationships', component: relationships, beforeEnter: requireAuth,
				children: [
					{path: 'list', name: 'List_Relationships', component: list_relationships, beforeEnter: requireAuth},
					{path: 'add', name: 'Add_Relationships', component: add_relationships, beforeEnter: requireAuth},
					{path: '', component: list_relationships, beforeEnter: requireAuth},
					{path: '*', redirect: 'list', beforeEnter: requireAuth}
				]
			},
			{path: 'visualisation', name: 'Visualisation',component: visualisation, beforeEnter: requireAuth},
			{path: 'share', name: 'Share', component: share, beforeEnter: requireAuth},
			{path: '*', redirect: 'overview', beforeEnter: requireAuth}
		]
	}
]

const router = new VueRouter({
	routes: routes
})

router.beforeEach(function(to, from, next) {
	HTTP.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('id_token')
	next()
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
		var path = 'dashboard/overview'
		next({ path: path })
	} else {
		next()
	}
}

var vm = new Vue({
	el: '#app',
	router: router,
	data: {
		authenticated: false,
		lock: new Auth0Lock('', '', {
			auth: {
				params: {
					scope: 'openid email'
				}
			}
		})
	},
	mounted: function() {
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
		},
		testSecured: function() {
			console.log('testing secured connection')
			HTTP.get('api/ping').then(
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