import colors from 'vuetify/es5/util/colors'

export default {
  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    titleTemplate: '%s - LinaEE',
    title: 'LinaEE',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },

  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: [],

  // Customize the progress-bar color
  loading: { color: '#de545f' },

  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: [],

  // Auto import components (https://go.nuxtjs.dev/config-components)
  components: true,

  // Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    '@nuxtjs/eslint-module',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify',
  ],

  // Modules (https://go.nuxtjs.dev/config-modules)
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    // '@nuxtjs/auth',
    // '@nuxtjs/proxy',
  ],

  // Axios module configuration (https://go.nuxtjs.dev/config-axios)
  axios: {
    // baseURL: 'http://192.168.1.46:8001/linapi/',
    baseURL: process.env.API_URL,
  },

  router: {
    middleware: ['auth_lina'],
  },

  // auth: {
  //   strategies: {
  //     local: {
  //       scheme: 'refresh',
  //       token: {
  //         property: 'access',
  //         maxAge: 1800,
  //         type: 'Bearer',
  //       },
  //       refreshToken: {
  //         property: 'refresh',
  //         data: 'refresh_token',
  //         maxAge: 60 * 60 * 24 * 7,
  //       },
  //       user: {
  //         property: false,
  //         autoFetch: true,
  //       },
  //       endpoints: {
  //         login: { url: 'login/', method: 'post' },
  //         refresh: { url: 'login_refresh/', method: 'post' },
  //         user: { url: 'user_perms/cur', method: 'get' },
  //         logout: false,
  //       },
  //       // autoLogout: false
  //     },
  //   },
  // },

  // proxy: {
  //   '/api': {
  //     target: 'http://192.168.1.46:8001/linapi',
  //     pathRewrite: {
  //       '^/api': '/',
  //     },
  //   },
  // },

  // Vuetify module configuration (https://go.nuxtjs.dev/config-vuetify)
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    treeShake: true,
    theme: {
      // options: {
      //   customProperties: true,
      // },
      dark: false,
      themes: {
        light: {
          primary: colors.azulCerceta.base,
          accent: colors.coral.base,
          secondary: colors.ambarSur.base,
          info: colors.indigo.accent3,
          warning: colors.amber.base,
          error: colors.red.base,
          success: colors.green.accent4,
        },
        dark: {
          primary: colors.azulCerceta.darken4,
          accent: colors.coral.darken3,
          secondary: colors.ambarSur.darken3,
          info: colors.indigo.accent3,
          warning: colors.amber.base,
          error: colors.red.base,
          success: colors.green.accent4,
        },
      },
    },
  },

  // Build Configuration (https://go.nuxtjs.dev/config-build)
  build: {
    analyze: true,
    extractCSS: true,
  },
}
