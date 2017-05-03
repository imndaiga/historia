var merge = require('webpack-merge')
var prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  AUTH0_ID: process.env.AUTH0_ID,
  AUTH0_DOMAIN: process.env.AUTH0_DOMAIN,
})
