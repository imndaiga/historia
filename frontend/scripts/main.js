// Create axios instance
var HTTP = axios.create({
	baseURL: ''
})

 var required = validators.required
 var email = validators.email
 var alpha = validators.alpha

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

Vue.prototype.$http = HTTP

function extendDict(obj, src) {
	for (key in src) {
		if (src.hasOwnProperty(key)) {
			obj[key] = src[key]
		}
		return obj
	}
}

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
		var path = 'dashboard/user'
		next({ path: path })
	} else {
		next()
	}
}

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
		},
		header: {
			type: Object,
			required: true
		},
		footer: {
			type: Array,
			required: true
		}
	}
})

Vue.component('app-mobile-menu', {
	template: "#app-mobile-menu",
	props: {
		current_panel: {
			type: String,
			required: true
		},
		panels: {
			type: Array,
			required: true
		},
		header: {
			type: Object,
			required: true
		},
		footer: {
			type: Array,
			required: true
		}
	},
	methods: {
		closeMobileMenu: function() {
			bus.$emit('close-mobile-menu')
		}
	}
})

Vue.component('app-header', {
	template: '#app-header',
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
		openMobileMenu: function() {
			document.getElementsByTagName('body')[0].classList.add('stop-scrolling')
			bus.$emit('open-mobile-menu')
		}
	}
})

Vue.component('app-menu', {
	template: '#app-menu',
	props: {
		current_panel: {
			type: String,
			required: true
		},
		panels: {
			type: Array,
			required: true
		},
		header: {
			type: Object,
			required: true
		},
		footer: {
			type: Array,
			required: true
		}
	},
	methods: {
		performAction: function(action) {
			if (action == 'logout') {
				this.$parent.$parent.$parent.logout()
			}
		}
	}
})

Vue.component('app-panel', {
	template: '#app-panel',
	props: {
		bs_panel: {
			type: Object,
			required: true
		}
	},
	methods: {
		bs_panel_selected: function(bs_panel) {
			bs_panel.open = !bs_panel.open
		}
	}
})

Vue.component('app-form', {
	template: '#app-form',
	props: {
		form : {
			type: Array,
			required: true
		},
		submit_type: {
			type: String,
			required: true
		}
	},
	data: function() {
		return {
			form_object: this.createFormObject(),
			sub_type: this.submit_type,
			picker: ''
		}
	},
	validations: function() {
		validations_dict = {}
		validations_dict['form_object'] = {}
		for (index in this.form) {
			key = this.form[index].field_name
			if (key != undefined) {
				validations_dict.form_object[key] = {}
				validations_dict.form_object[key].value = {}
				if (Object.keys(this.form[index]).indexOf('validators') != -1) {
					validators = this.form[index].validators
					validations_dict.form_object[key].value = validators
				}
			}
		}
		return validations_dict
	},
	methods: {
		submitForm: function() {
			if (!this.$v.$invalid) {
				var form_data = {}
				for (field in this.form_object) {
					form_data[field] = this.form_object[field].value
				}
				form_data['submit_type'] = this.sub_type
				this.$http.put('/api/relationships', {
					data: {
						form: form_data
					}
				}).then(
					function(response) {
						console.log(response)
						swal({
							title: 'Success',
							text: '',
							type: 'success',
							timer: 1500,
							showConfirmButton: false
						})
					},
					function(error) {
						console.log(error)
						swal({
							title: 'Ooops...',
							text: 'An error occured',
							type: 'error'
						})
					}
				)
			} else {
				this.$v.$touch()
				swal({
					title: 'Ooops...',
					text: 'Form not filled in correctly',
					type: 'error',
					timer: 2000,
					showConfirmButton: false
				})
			}
		},
		asyncFind: function(field_name, value) {
			var self = this
			var field = field_name
			var value = value
			this.form_object[field_name].loading = true
			this.$forceUpdate()
			this.$http.get('/api/search', {
				params: {
					field: field,
					value: value
				}
			}).then(
				function(response) {
					self.form_object[field_name].loading = false
					self.$forceUpdate()
					if (Object.keys(response.data).length > 0) {
						self.form_object[field_name].options = [response.data.fullname]
					} else {
						self.form_object[field_name].options = []
					}
				},
				function(error) {
					self.form_object[field_name].loading = false
					self.$forceUpdate()
					console.log(error)
				}
			)
		},
		createFormObject: function() {
			var form_object = {}
			for (index in this.form) {
				key = this.form[index].field_name
				if (this.form[index].type != 'submit-button') {
					form_object[key] = {}
					if (this.form[index].type == 'search-input') {
						form_object[key]['loading'] = false
						form_object[key]['options'] = []
					}
					if (Object.keys(this.form[index]).indexOf('value') != -1) {
						form_object[key]['value'] = this.form[index].value
					} else {
						form_object[key]['value'] = ''
					}
				}
			}
			return form_object
		}
	},
	computed: {
		pikaday_Hooks: function() {
			hooks = []
			if (Object.keys(this.$refs).length == 2) {
				for (ref in this.$refs) {
					if (ref.indexOf('-btn') == -1) {
						hooks.push(ref)
					}
					hooks.push(this.$refs[ref])
				}
			} else {
				return null
			}
			return hooks
		},

	},
	mounted: function() {
		var self = this
		if (this.pikaday_Hooks) {
			for (index in this.pikaday_Hooks) {
				if (typeof this.pikaday_Hooks[index] === 'string') {
					var pikaday_field_name = this.pikaday_Hooks[index]
					this.pikaday_Hooks.splice(index, 1)
				}
			}
			this.picker = new Pikaday({
				ref: this.base_ref,
				field: this.pikaday_Hooks[0][0],
				trigger: this.pikaday_Hooks[1][0],
				onSelect: function() {
					date = this.getMoment().format('Do MMMM YYYY')
					self.form_object[pikaday_field_name].value = date
				}
			})
		}
	}
})

Vue.component('app-table', {
	template: '#app-table',
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
		openRelation: function(person_id) {
			bus.$emit('open-modal', person_id)
		},
		deleteRelation: function(person_id) {
			bus.$emit('delete-relation', person_id)
		}
	}
})

Vue.component('modal-window', {
	template: '#modal-window',
	methods: {
		closeModal: function() {
			bus.$emit('close-modal')
		},
		submitForm: function() {
			this.$children[0].submitForm()
		}
	}
})

Vue.component('multiselect', VueMultiselect.default)

const dashboard = Vue.component('dashboard-page', {
	template: '#dashboard-page',
	data: function() {
		return {
			open_mobile_menu: false,
			sidebar_header: {
				title: 'MIMINANI',
				logo: 'fa fa-tree fa-lg'
			},
			sidebar_panels : [
				{
					name: 'User',
					navs: [
						{
							title: 'Profile',
							info: 'Your profile',
							view: 'User',
							id: 1
						},
						{
							title: 'Settings',
							info: 'Configure your profile settings',
							view: 'User',
							id: 2
						}
					],
					default_view: 'User',
					icon: 'fa fa-user-circle-o fa-lg',
					id: 1
				},
				{
					name: 'Visualisation',
					navs: [],
					icon: 'fa fa-eye fa-lg',
					id: 2
				},
				{
					name: 'Relationships',
					navs: [
						{
							title: 'List Relationships',
							info: 'List all your relationships',
							view: 'List_Relationships',
							id: 1
						},{
							title: 'Add Relationships',
							info: 'Add a relationship to your tree',
							view: 'Add_Relationships',
							id: 2
						}
					],
					default_view: 'List_Relationships',
					icon: 'fa fa-globe fa-lg',
					id: 3
				}
			],
			sidebar_footer: [
				{
					type: 'footer_button',
					caption:'Log Out',
					action: 'logout',
					class: 'btn btn-block btn-lg btn-warning',
					reference: 'Your Profile'
				},
				{
					type: 'footer_link',
					path_type: 'internal',
					caption: 'Info',
					icon: 'fa fa-info-circle fa-lg',
					link: 'List_Relationships',
					reference: 'Read more about the miminani project'
				},
				{
					type: 'footer_link',
					path_type: 'external',
					caption: 'Github',
					icon: 'fa fa-github-alt fa-lg',
					link: 'https://github.com/squarenomad/miminani',
					reference: 'View our open source code'
				},
			]
		}
	},
	created: function() {
		bus.$on('open-mobile-menu', function() {
			this.open_mobile_menu = true
		}.bind(this))
		bus.$on('close-mobile-menu', function() {
			this.open_mobile_menu = false
		}.bind(this))
	},
	computed: {
		current_Panel: function() {
			return this.$route.path.split('/')[2].charAt(0).toUpperCase() + this.$route.path.split('/')[2].slice(1)
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
				// {type: 'multiselect-input', placeholder: 'Select Country', label: 'Country of Origin',
				// 	multiselect_options: ['Kenya', 'Uganda', 'Tanzania'],
				// 	validators: {required}, field_name: 'origin_country'}
			],
			particlesjs_data : {
				"particles": {
				    "number": {"value": 30, "density": { "enable": true, "value_area": 800}},
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
				{name: 'add_relative_panel', open: false, label: 'Add Relative', icon: 'fa fa-user-plus fa-lg'},
				{name: 'add_relationship_panel', open: false, label: 'Add Relationship', icon: 'fa fa-link fa-lg'}],
			form_data: [
				{type: 'alpha-input', placeholder: 'Enter First Name', label: 'First Name', bs_panel: 'add_relative_panel', validators: { required, alpha }, field_name: 'first_name', id: 1},
				{type: 'alpha-input', placeholder: 'Enter Ethnic Name', label: 'Ethnic Name', bs_panel: 'add_relative_panel', validators: { required, alpha }, field_name: 'ethnic_name', id: 2},
				{type: 'alpha-input', placeholder: 'Enter Last Name', label: 'Last Name', bs_panel: 'add_relative_panel', validators: { required, alpha }, field_name: 'last_name', id: 3},
				{type: 'email-input', placeholder: 'Enter Email Address', label: 'Email', bs_panel: 'add_relative_panel', validators: { email }, field_name: 'email', id: 4},
				{type: 'search-input', placeholder: 'Search for Relative', label: 'Relative',
					multiselect_options: [],
					bs_panel: 'add_relationship_panel', validators: {required}, field_name: 'relation_person', id: 4
				},
				{type: 'multiselect-input', placeholder: 'Choose a Relation', label: 'Relation',
					multiselect_options: ['Father', 'Mother', 'Sister', 'Brother', 'Step-Father', 'Step-Mother', 'Step-Sister', 'Step-Brother', 'Daughter', 'Son'],
					bs_panel: 'add_relationship_panel', validators: {required}, field_name: 'relation_name', id: 5
				},
				{type: 'pikaday-input', placeholder: 'Select Birth Date', label: 'Date of Birth', bs_panel: 'add_relative_panel', validators: {required}, field_name: 'birth_date', id: 6},
				{type: 'submit-button', button_message: 'Save Relative', button_name: 'add_personal-details', bs_panel: 'add_relative_panel', button_class: 'btn btn-lg btn-success btn-block btn-margin', id: 7},
				{type: 'submit-button', button_message: 'Save Relationship', button_name: 'add_connect-relations', bs_panel: 'add_relationship_panel', button_class: 'btn btn-lg btn-success btn-block btn-margin', id: 8}

			]
		}
	},
	methods: {
		splitPanelForm: function(form_data, bs_panel) {
			split_form = []
			for (index in form_data) {
				if (form_data[index].bs_panel == bs_panel) {
					split_form.push(form_data[index])
				}
			}
			return split_form
		}
	}
})

const list_relationships = Vue.component('list-relationships-page', {
	template: '#list-relationships-page',
	data: function() {
		return {
			modal_open: false,
			modal_form_data: [],
			relative_data: [],
			resource_url: '/api/relationships',
			options: {
				headers: {
					'Authorization': 'Bearer ' + localStorage.getItem('id_token')
				},
				next_button_text: '',
				previous_button_text: ''
			}
		}
	},
	methods: {
		updateTable: function(data) {
			this.relative_data = data
			this.$forceUpdate()
		},
		getModalData: function(person_id) {
				var self = this
				this.$http.get('/api/person', {
					params: {
						id: person_id
					}
				}).then(
				function(response) {
					self.modal_form_data = response.data
					self.$forceUpdate()
					self.modal_open = true
				},
				function(error) {
					console.log(error)
				}
			)
		}
	},
	computed: {
		table_Headers: function() {
			headers = []
			for (relative in this.relative_data) {
				for (field in this.relative_data[relative]) {
					header = this.relative_data[relative][field].label
					if (headers.indexOf(header) == -1 && header != 'ID') {
						headers.push(this.relative_data[relative][field].label)
					}
				}
			}
			return headers
		},
		table_Data: function() {
			relations = []
			entry = {}
			for (relative in this.relative_data) {
				for (field in this.relative_data[relative]) {
					field_name = this.relative_data[relative][field].field_name
					field_value = this.relative_data[relative][field].value
					entry[field_name] = field_value
				}
				relations.push(entry)
				entry = {}
			}
			return relations
		}
	},
	created: function() {
		bus.$on('open-modal', function(person_id) {
			document.getElementsByTagName('body')[0].classList.add('stop-scrolling')
			this.getModalData(person_id)
		}.bind(this))
		bus.$on('close-modal', function() {
			document.getElementsByTagName('body')[0].classList.remove('stop-scrolling')
			this.modal_open = false
		}.bind(this))
		bus.$on('delete-relation', function(person_id) {
			var self = this
			swal({
				title: 'Are you sure?',
				text: 'Deleted relations cannot be recovered!',
				type: 'warning',
				showCancelButton: true,
				confirmButtonText: 'Delete',
				closeOnConfirm: false
			},
			function() {
				self.$http.delete('/api/relationships', {
					data: {
						user_id: person_id
					}
				}).then(
					function(response) {
						for (index in self.relative_data) {
							for (field in self.relative_data[index]) {
								if (self.relative_data[index][field].field_name == 'id') {
									if (self.relative_data[index][field].value == person_id) {
										self.relative_data.splice(index, 1)
										self.$forceUpdate()
									}
								}
							}
						}
						swal({
							title: 'Deleted',
							text: 'Relation has successfully been deleted',
							type: 'success',
							timer: 1500,
							showConfirmButton: false,
							customClass: 'message-height'
						})
					},
					function(response) {
						console.log(response)
						swal({
							title: 'Ooops...',
							text: 'An error occured',
							type: 'error'
						})
					}
				)
			})
		}.bind(this))
	}
})

const visualisation = Vue.component('visualisation-page', {
	template: '#visualisation-page',
	data: function() {
		return {
			graph: {}
		}
	},
	methods: {
		renderGraph: function() {
			var s = new sigma({
				graph: this.graph,
				container: 'sigma-container',
				settings: {
		            defaultLabelSize: 20,
		            font: 'Open Sans',
		            labelThreshold: 12
		        }
			})
			var dragListener = sigma.plugins.dragNodes(s, s.renderers[0])
		}
	},
	created: function() {
		var self = this
		this.$http.get('/api/graph').then(
			function(response) {
				self.graph = response.data.graph
				self.renderGraph()
				self.$forceUpdate()
			},
			function(error) {
				console.log(error)
			}
		)
	}
})

const user = Vue.component('user-page', {
	template: '#user-page'
})

Vue.component('v-paginator', VuePaginator)

const routes = [
	{ path: '/', component: welcome, beforeEnter: autoRoute},
	{ path: '/dashboard', component: dashboard, beforeEnter: requireAuth,
		children: [
			{path: 'relationships', component: relationships, beforeEnter: requireAuth,
				children: [
					{path: 'list', name: 'List_Relationships', component: list_relationships, beforeEnter: requireAuth},
					{path: 'add', name: 'Add_Relationships', component: add_relationships, beforeEnter: requireAuth},
					{path: '', component: list_relationships, beforeEnter: requireAuth},
					{path: '*', redirect: 'list', beforeEnter: requireAuth}
				]
			},
			{path: 'visualisation', name: 'Visualisation', component: visualisation, beforeEnter: requireAuth},
			{path: 'user', name: 'User', component: user, beforeEnter: requireAuth},
			{path: '*', redirect: 'user', beforeEnter: requireAuth}
		]
	}
]

const router = new VueRouter({
	routes: routes
})

router.beforeEach(
	function(to, from, next) {
		Vue.prototype.$http.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('id_token')
		bus.$emit('close-mobile-menu')
		next()
})

var bus = new Vue()

Vue.use(window.vuelidate.default)

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
			this.$http.get('api/ping').then(
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