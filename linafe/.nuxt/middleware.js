const middleware = {}

middleware['auth_lina'] = require('../middleware/auth_lina.js')
middleware['auth_lina'] = middleware['auth_lina'].default || middleware['auth_lina']

middleware['logged_in_lina'] = require('../middleware/logged_in_lina.js')
middleware['logged_in_lina'] = middleware['logged_in_lina'].default || middleware['logged_in_lina']

export default middleware
