const Nuxt = require('nuxt')
const bodyParser = require('body-parser')
const session = require('express-session')
const express = require('express')
const passport = require('passport')
const LocalStrategy = require('passport-local').Strategy
const appData = require('./data.json')

const host = process.env.HOST || '127.0.0.1'
const port = process.env.PORT || 3000
const sessionSecret = process.env.SECRET || 'ncdunioubaiub9287&@!'

const userData = appData.users

function getUser (email) {
  const user = userData.find(function (user) {
    return user.email === email
  })
  return Object.assign({}, user)
}

const server = express()

server.use(bodyParser.json())
server.use(session({
  secret: sessionSecret,
  resave: false,
  saveUninitialized: false,
  cookie: { maxAge: 60000 }
}))
server.use(passport.initialize())
server.use(passport.session())

passport.use(new LocalStrategy({
    usernameField: 'email',
    passwordField: 'password'
  },
  function (email, password, done) {
    const user = getUser(email)

    if (!user || user.password !== password) {
      return done(null, false)
    }

    delete user.password
    return done(null, user)
  }
))

passport.serializeUser(function (user, done) {
  return done(null, user.email)
})

passport.deserializeUser(function (email, done) {
  const user = getUser(email)
  delete user.password
  return done(null, user)
})

const authRoutes = express.Router()

authRoutes.post('/login', function(req, res, next) {
  passport.authenticate('local', function (err, user, info) {
    if (err) { return next(err) }
    if (!user) { return res.status(401).json({ error: 'Bad credentials' }) }
    req.logIn(user, function(err) {
      if (err) { return next(err) }
      req.session.authUser = { user: user.email }
      return res.json({ user: user.email })
    })
  })(req, res, next)
})

authRoutes.post('/logout', function (req, res) {
  req.logout()
  delete req.session.authUser
  res.json({ user: req.user })
})

server.use('/auth', authRoutes)

const config = require('./nuxt.config.js')
config.dev = !(process.env.NODE_ENV === 'production')

const nuxt = new Nuxt(config)

if (config.dev) {
  nuxt.build()
  .catch( function (error) {
    console.log(error) // eslint-disable-line no-console
    process.exit(1)
  })
}

server.use(nuxt.render)
server.listen(port, host)
console.log('Server is listening on ' + host + ':' + port) // eslint-disable-line no-console
