const Nuxt = require('nuxt')
const bodyParser = require('body-parser')
const session = require('express-session')
const app = require('express')()
const host = process.env.HOST || '127.0.0.1'
const port = process.env.PORT || 3000
const sessionSecret = process.env.SECRET || 'ncdunioubaiub9287&@!'

app.set('port', port)

app.use(bodyParser.json())

app.use(session({
	secret: sessionSecret,
	resave: false,
	saveUninitialized: false,
	cookie: { maxAge: 60000 }
}))

app.post('/api/login', function (req, res) {
	if (req.body.data.email === 'demo@gmail.com' && req.body.data.password === 'demo') {
		req.session.authUser = { username: 'demo' }
		return res.json({ username: 'demo' })
	}
	res.status(401).json({ error: 'Bad credentials' })
})

app.post('/api/logout', function (req, res) {
	delete req.session.authUser
	res.json({ ok: true })
})

var config = require('./nuxt.config.js')
config.dev = !(process.env.NODE_ENV === 'production')

const nuxt = new Nuxt(config)

if (config.dev) {
	nuxt.build()
	.catch( function (error) {
		console.log(error) // eslint-disable-line no-console
		process.exit(1)
	})
}

app.use(nuxt.render)
app.listen(port, host)
console.log('Server is listening on ' + host + ':' + port) // eslint-disable-line no-console
