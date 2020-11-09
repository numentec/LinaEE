const middleware = {}

middleware['auth_lina'] = require('../middleware/auth_lina.js')
middleware['auth_lina'] = middleware['auth_lina'].default || middleware['auth_lina']

middleware['guest'] = require('../middleware/guest.js')
middleware['guest'] = middleware['guest'].default || middleware['guest']

export default middleware
