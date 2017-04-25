const Nuxt = require('nuxt')
const express = require('express')
const port = process.env.PORT || 3000
const server = express()

const config = require('./nuxt.config.js')
config.dev = !(process.env.NODE_ENV === 'production')

const nuxt = new Nuxt(config)

if (config.dev) {
  nuxt.build()
  .catch(function (error) {
    console.log(error) // eslint-disable-line no-console
    process.exit(1)
  })
}

server.use(nuxt.render)
server.listen(port, function () {
  console.log('Server is listening on port: ' + port) // eslint-disable-line no-console
})
