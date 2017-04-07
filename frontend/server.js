const Nuxt = require('nuxt')
const bodyParser = require('body-parser')
const express = require('express')
const passport = require('passport')
const passportJWT = require('passport-jwt')
const jwt = require('jsonwebtoken')
const jwtStrategy = passportJWT.Strategy
const ExtractJwt = passportJWT.ExtractJwt

const appData = require('./data.json')
const port = process.env.PORT || 3000
const jwtSecret = process.env.JWTSECRET || 'ncdunioubaiub9287&@!'

const userData = appData.users

function getUser (email, id) {
  var field
  var data
  if (email && !id) {
    field = 'email'
    data = email
  } else if (!email && id) {
    field = 'id'
    data = id
  } else {
    return null
  }
  const user = userData.find(function (user) {
    return user[field] === data
  })
  return Object.assign({}, user)
}

const server = express()

server.use(bodyParser.json())
server.use(passport.initialize())

const jwtOptions = {
  jwtFromRequest: ExtractJwt.fromAuthHeader(),
  secretOrKey: jwtSecret
}

var strategy = new jwtStrategy(jwtOptions, function (payload, done) {
  var user = getUser(null, payload.id)

  if (user) {
    delete user.password
    done(null, user)
  } else {
    done(null, false)
  }
})

passport.use(strategy)

const authRoutes = express.Router()

authRoutes.post('/login', function (req, res) {
  if (req.body.email && req.body.password) {
    var email = req.body.email
    var password = req.body.password
    var user = getUser(email, null)

    if (!user) { res.status(401).json({ error: 'Bad credentials' }) }

    if (user.password === password) {
      delete user.password
      var payload = { id: user.id }
      var token = jwt.sign(payload, jwtOptions.secretOrKey)
      res.json({
        token: token,
        user: user
      })
    } else {
      res.status(401).json({ error: 'Bad credentials' })
    }
  } else {
    res.status(401).json({ error: 'Bad credentials' })
  }
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
server.listen(port, function () {
  console.log('Server is listening on port: ' + port) // eslint-disable-line no-console
})
