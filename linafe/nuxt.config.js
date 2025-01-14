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
  css: [
    'devextreme/dist/css/dx.common.css',
    '~/assets/dxstyles/dx.material.linaee_cerceta_compact.css',
    // 'devextreme/dist/css/dx.light.css',
  ],

  // Customize the progress-bar color
  loading: { color: 'success', height: '5px' },

  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: ['~/plugins/saveRoute.js', '~/plugins/cartState.js'],

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
    '@nuxtjs/auth',
  ],

  // Axios module configuration (https://go.nuxtjs.dev/config-axios)
  axios: {
    baseURL: process.env.API_URL_SERVER,
    browserBaseURL: process.env.API_URL_CLIENT,
  },

  auth: {
    redirect: {
      login: '/login',
      logout: '/login',
      home: '/',
    },
    strategies: {
      local: {
        endpoints: {
          login: { url: 'login/', method: 'post' },
          user: { url: 'user_perms/cur', method: 'get' },
          logout: { url: 'logout/', method: 'post' },
        },
        autoFetchUser: false,
        tokenType: 'Token',
      },
    },
  },

  router: {
    // base: '/lina/',
    middleware: ['auth'],
    prefetchLinks: false,
  },

  // Vuetify module configuration (https://go.nuxtjs.dev/config-vuetify)
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    treeShake: true,
    theme: {
      options: {
        customProperties: true,
      },
      dark: false,
      themes: {
        light: {
          primary: '#047c9e',
          accent: '#d72839',
          secondary: '#ffb300',
          info: colors.indigo.accent3,
          warning: colors.amber.base,
          error: colors.red.base,
          success: colors.green.accent4,
          asgrey: '#9FD5D1',
          asgrey2: '#A5C9C7',
          formtabs: '#CCE4EB',
          pricomplementary: '#9E2604',
        },
        dark: {
          primary: '#022a31',
          accent: '#561017',
          secondary: '#664700',
          info: colors.indigo.accent3,
          warning: colors.amber.base,
          error: colors.red.base,
          success: colors.green.accent4,
          asgrey: '#79AFAB',
        },
      },
    },
  },

  // Build Configuration (https://go.nuxtjs.dev/config-build)
  build: {
    standalone: true,
    analyze: process.env.ANALIZE,
    extractCSS: true,
  },

  publicRuntimeConfig: {
    browserBaseURL: process.env.API_URL_CLIENT,
    publicURL: process.env.PUBLIC_URL,
    fotosURL: process.env.FOTOS_URL,
    fotosExt: process.env.FOTOS_EXT,
    mediaURL: process.env.MEDIA_URL,
  },
  privateRuntimeConfig: {},
}
