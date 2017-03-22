// HELPER FUNCTIONS AND SETUP

var HTTP = axios.create({
	// Create axios instance
	baseURL: ''
})

 var required = validators.required
 var email = validators.email
 var alpha = validators.alpha

HTTP.interceptors.response.use(
	// Set up axios interceptors to error responses
	function(response) {
		return response
	},
	function(error) {
		// Do something with response error
		bus.$emit('clear-children')
		if (!!error.response && error.response.status === 401) {
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
		swal({
			title: 'Ooops...',
			text: 'Please check your Internet connection',
			type: 'error'
		})
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

// APP COMPONENTS

Vue.component('app-sidebar-menu', {
	template: "#app-sidebar-menu",
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
			document.getElementsByTagName('body')[0].classList.remove('stop-scrolling')
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
	data: function() {
		return {
			open_submenu: this.current_panel
		}
	},
	methods: {
		performAction: function(action) {
			if (action == 'logout') {
				this.$parent.$parent.$parent.logout()
			}
		},
		setOpenSubmenu: function(panel_name) {
			this.open_submenu = panel_name
			this.$forceUpdate()
			document.getElementsByTagName('body')[0].classList.remove('stop-scrolling')
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
	mixins: [window.vuelidate.validationMixin],
	components: {
		'multiselect': VueMultiselect.default
	},
	props: {
		form : {
			type: Array,
			required: true
		},
		submit_resource: {
			type: String,
			required: true
		},
		search_resource: {
			type: String,
			required: true
		},
		form_is_inline: {
			type: Boolean,
			required: true
		}
	},
	data: function() {
		return {
			form_object: this.createFormObject(),
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
				this.$http.put(this.submit_resource, {
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
			}
		},
		asyncFind: function(field_name, value) {
			var self = this
			var field = field_name
			var value = value
			this.form_object[field_name].loading = true
			this.$forceUpdate()
			this.$http.get(this.search_resource, {
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
					form_object[key]['activated'] = false
				}
			}
			return form_object
		},
		activateField: function(field_name) {
			this.form_object[field_name].activated = true
			bus.$emit('form-field-activated')
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
	components: {
		'v-paginator': VuePaginator
	},
	props: {
		resource_url: {
			type: String,
			required: true
		}
	},
	data: function() {
		return {
			raw_table_data: [],
			options: {
				headers: {
					'Authorization': 'Bearer ' + localStorage.getItem('id_token')
				},
				next_button_text: '',
				previous_button_text: ''
			},
			table_loaded: false
		}
	},
	methods: {
		updateTable: function(data) {
			this.raw_table_data = data
			this.$forceUpdate()
			this.table_loaded = true
			bus.$emit('table-loaded')
		},
		openRecordInModal: function(person_id, person_name_list, resource_name) {
			full_name = person_name_list.filter(function(val) {return val}).join(' ')
			bus.$emit('open-modal', person_id, resource_name, full_name)
		},
		deleteRecord: function(record_id) {
			var self = this
			swal(
			{
				title: 'Are you sure?',
				text: 'This cannot be undone!',
				type: 'warning',
				showCancelButton: true,
				confirmButtonText: 'Delete',
				closeOnConfirm: false
			},
			function() {
				self.$http.delete(self.resource_url, {
					data: {
						id: record_id
					}
				}).then(
					function(response) {
						swal({
							title: 'Complete',
							text: 'Successfully deleted!',
							type: 'success',
							timer: 1500,
							showConfirmButton: false,
							customClass: 'message-height'
						})
						for (record in self.raw_table_data) {
							for (field in self.raw_table_data[record]) {
								if (self.raw_table_data[record][field].field_name == 'id') {
									if (self.raw_table_data[record][field].value == record_id) {
										self.raw_table_data.splice(record, 1)
										self.$forceUpdate()
									}
								}
							}
						}
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
			})
		}
	},
	computed: {
		table_Headers: function() {
			headers = []
			for (record in this.raw_table_data) {
				for (field in this.raw_table_data[record]) {
					header = this.raw_table_data[record][field].label
					if (headers.indexOf(header) == -1 && header != 'ID') {
						headers.push(this.raw_table_data[record][field].label)
					}
				}
			}
			return headers
		},
		table_Data: function() {
			records = []
			entry = {}
			for (record in this.raw_table_data) {
				for (field in this.raw_table_data[record]) {
					field_name = this.raw_table_data[record][field].field_name
					field_value = this.raw_table_data[record][field].value
					entry[field_name] = field_value
				}
				records.push(entry)
				entry = {}
			}
			return records
		}
	},
	created: function() {
		bus.$on('clear-children', function() {
			this.table_loaded = true
		}.bind(this))
	}
})

Vue.component('app-modal-form', {
	template: '#app-modal-form',
	props: {
		resource_urls: {
			type: Object,
			required: true
		}
	},
	data: function() {
		return {
			modal_open: false,
			raw_modal_form_data: [],
			activate_submit_button: false,
			resource_url: '',
			inlined_form: false,
			modal_title: ''
		}
	},
	methods: {
		closeModal: function() {
			self.raw_modal_form_data = []
			this.modal_open = false
			this.activate_submit_button = false
			this.modal_title = ''
			document.getElementsByTagName('body')[0].classList.remove('stop-scrolling')
		},
		getModalFormData: function(record_id) {
				var self = this
				this.$http.get(this.resource_url, {
					params: {
						id: record_id
					}
				}).then(
				function(response) {
					self.raw_modal_form_data = response.data.form
					self.inlined_form = response.data.inline
					self.$forceUpdate()
					self.modal_open = true
				},
				function(error) {
					console.log(error)
				}
			)
		},
		submitForm: function() {
			this.$children[0].submitForm()
		}
	},
	created: function() {
		bus.$on('open-modal', function(record_id, resource_name, title) {
			for (url in this.resource_urls) {
				if (url == resource_name) {
					this.resource_url = this.resource_urls[url]
				}
			}
			document.getElementsByTagName('body')[0].classList.add('stop-scrolling')
			this.modal_title = title
			this.getModalFormData(record_id)
		}.bind(this))
		bus.$on('form-field-activated', function() {
			this.activate_submit_button = true
		}.bind(this))
	},
	computed: {
		modal_Form_Data: function() {
			processed = this.raw_modal_form_data
			for (field in this.raw_modal_form_data) {
				if (this.raw_modal_form_data[field].validators != undefined) {
					field_validators = this.raw_modal_form_data[field].validators
					processed[field].validators = {}
					for (index in field_validators) {
						if (field_validators[index] == 'required') {
							processed[field].validators = extendDict(processed[field].validators, {required})
						} else if (field_validators[index] == 'alpha') {
							processed[field].validators = extendDict(processed[field].validators, {alpha})
						} else if (field_validators[index] == 'email') {
							processed[field].validators = extendDict(processed[field].validators, {email})
						}
					}
				}
			}
			return processed
		}
	}
})

Vue.component('app-loading', {
	template: '#app-loading',
	props: {
		is_loading: {
			type: Boolean,
			required: true
		}
	}
})

// APP NAVIGATION PAGES

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
							view: 'Profile',
							id: 1
						},
						{
							title: 'Settings',
							info: 'Configure your profile settings',
							view: 'Settings',
							id: 2
						}
					],
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
					reference: 'Read more about the miminani project',
					key: 1
				},
				{
					type: 'footer_link',
					path_type: 'external',
					caption: 'Github',
					icon: 'fa fa-github-alt fa-lg',
					link: 'https://github.com/squarenomad/miminani',
					reference: 'View our open source code',
					key: 2
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
		bus.$on('clear-children', function() {
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
			submit_resource: 'api/relationships?type=add',
			search_resource: 'api/search',
			bs_panels: [
				{name: 'add_relative_panel', open: false, label: 'Add Relative', icon: 'fa fa-user-plus fa-lg'},
				{name: 'add_relationship_panel', open: false, label: 'Add Relationship', icon: 'fa fa-link fa-lg'}],
			form_data: [
				{type: 'alpha-input', placeholder: 'Enter First Name', label: 'First Name', bs_panel: 'add_relative_panel', validators: { required, alpha }, field_name: 'first_name', classes: '' , id: 1},
				{type: 'alpha-input', placeholder: 'Enter Ethnic Name', label: 'Ethnic Name', bs_panel: 'add_relative_panel', validators: { required, alpha }, field_name: 'ethnic_name', classes: '' , id: 2},
				{type: 'alpha-input', placeholder: 'Enter Last Name', label: 'Last Name', bs_panel: 'add_relative_panel', validators: { required, alpha }, field_name: 'last_name', classes: '' , id: 3},
				{type: 'email-input', placeholder: 'Enter Email Address', label: 'Email', bs_panel: 'add_relative_panel', validators: { email }, field_name: 'email', classes: '' , id: 4},
				{type: 'search-input', placeholder: 'Search for Relative', label: 'From', bs_panel: 'add_relationship_panel', validators: {required}, field_name: 'from_person', classes: '' , 'SelectLabel': '', 'DeselectLabel': '', id: 5},
				{type: 'search-input', placeholder: 'Search for Relative', label: 'To', bs_panel: 'add_relationship_panel', validators: {required}, field_name: 'to_person', classes: '' , 'SelectLabel': '', 'DeselectLabel': '', id: 6},
				{type: 'multiselect-input', placeholder: 'Choose a Relation', label: 'Relation', bs_panel: 'add_relationship_panel', validators: {required}, field_name: 'relation_name', classes: '' , id: 7,
					multiselect_options: ['Parent', 'Partner', 'Sibling', 'Step-Parent', 'Step-Sibling', 'Child'], 'SelectLabel': '', 'DeselectLabel': '',
				},
				{type: 'pikaday-input', placeholder: 'Select Birth Date', label: 'Date of Birth', bs_panel: 'add_relative_panel', field_name: 'birth_date', classes: '' , id: 8},
				{type: 'submit-button', button_message: 'Save Relative', button_name: 'add_personal-details', bs_panel: 'add_relative_panel', button_class: 'btn btn-lg btn-success btn-block btn-margin', id: 9},
				{type: 'submit-button', button_message: 'Save Relationship', button_name: 'add_connect-relations', bs_panel: 'add_relationship_panel', button_class: 'btn btn-lg btn-success btn-block btn-margin', id: 10}

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
			modal_resources: {
				record_resource: '/api/person',
				links_resource: '/api/person/family',
				submit_resource: 'api/relationships?type=mod',
				search_resource: 'api/search'
			},
			table_resource: '/api/relationships',
			loading: true
		}
	},
	created: function() {
		bus.$on('table-loaded', function() {
			this.loading = false
		}.bind(this))
		bus.$on('clear-children', function() {
			this.loading = false
		}.bind(this))
	}
})

const visualisation = Vue.component('visualisation-page', {
	template: '#visualisation-page',
	data: function() {
		return {
			graph: {},
			resource_url: '/api/graph',
			loading: false,
			viz: { graph: ''}
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
			s.startForceAtlas2({worker: true, barnesHutOptimize: false})
			this.viz = s
		}
	},
	computed: {
		graph_Has_Nodes: function() {
			if (!!this.viz.graph.nodes) {
				return true
			} else {
				return false
			}
		}
	},
	created: function() {
		this.loading = true
		var self = this
		this.$http.get(this.resource_url).then(
			function(response) {
				self.graph = response.data.graph
				self.renderGraph()
				self.$forceUpdate()
				self.loading = false
			},
			function(error) {
				console.log(error)
				self.loading = false
			}
		)
	}
})

const user = Vue.component('user-page', {
	template: '#user-page',
	data: function() {
		return {
			loading: true
		}
	}
})

const user_profile = Vue.component('user-profile-page', {
	template: '#user-profile-page',
	data: function() {
		return {
			loading: true
		}
	}
})

const user_settings = Vue.component('user-settings-page', {
	template: '#user-settings-page',
	data: function() {
		return {
			loading: true
		}
	}
})

// ROUTER CONFIG

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
			{path: 'user', component: user, beforeEnter: requireAuth,
				children: [
					{path: 'profile', name: 'Profile', component: user_profile, beforeEnter: requireAuth},
					{path: 'settings', name: 'Settings', component: user_settings, beforeEnter: requireAuth},
					{path: '', component: user_profile, beforeEnter: requireAuth},
					{path: '*', redirect: 'profile', beforeEnter: requireAuth}
				]
			},
			{path: '*', redirect: 'profile', beforeEnter: requireAuth}
		]
	}
]

const router = new VueRouter({
	routes: routes
})

router.beforeEach(
	function(to, from, next) {
		Vue.prototype.$http.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('id_token')
		bus.$emit('clear-children')
		next()
})

// VUE INSTANCE CONFIGS

var bus = new Vue()

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
				} else {
					// Set the token and user profile in local storage
					localStorage.setItem('profile', JSON.stringify(profile))
				}
			})
			self.authenticated = true
			self.$router.push('/dashboard/user')
		})
		this.lock.on('authorization_error', function(error) {
			// handle error when authorizaton fails
			console.log('authorization error')
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
			this.$router.push('/')
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
	}
})