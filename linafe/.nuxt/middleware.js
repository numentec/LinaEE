const middleware = {}

middleware['auth_lina'] = require('../middleware/auth_lina.js')
middleware['auth_lina'] = middleware['auth_lina'].default || middleware['auth_lina']

export default middleware
