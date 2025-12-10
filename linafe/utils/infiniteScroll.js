/**
 * Composable para infinite scrolling
 * Útil para reutilizar la lógica de infinite scroll en otros componentes
 */

export function useInfiniteScroll(options = {}) {
  const {
    threshold = 200,
    throttleDelay = 100,
    onLoadMore = () => {},
    shouldLoadMore = () => false,
  } = options

  let scrollTimeout = null

  const handleScroll = () => {
    if (scrollTimeout) return

    scrollTimeout = setTimeout(() => {
      checkScrollPosition()
      scrollTimeout = null
    }, throttleDelay)
  }

  const checkScrollPosition = () => {
    const scrollHeight = document.documentElement.scrollHeight
    const scrollTop = document.documentElement.scrollTop
    const clientHeight = document.documentElement.clientHeight

    const nearBottom = scrollTop + clientHeight >= scrollHeight - threshold

    if (nearBottom && shouldLoadMore()) {
      onLoadMore()
    }
  }

  const handleResize = () => {
    // Usar nextTick si está disponible (Vue), si no usar setTimeout
    const nextTick = window.Vue?.$nextTick || ((fn) => setTimeout(fn, 0))
    nextTick(() => {
      checkScrollPosition()
    })
  }

  const bindEvents = () => {
    window.addEventListener('scroll', handleScroll, { passive: true })
    window.addEventListener('resize', handleResize)
  }

  const unbindEvents = () => {
    window.removeEventListener('scroll', handleScroll)
    window.removeEventListener('resize', handleResize)
    if (scrollTimeout) {
      clearTimeout(scrollTimeout)
      scrollTimeout = null
    }
  }

  return {
    bindEvents,
    unbindEvents,
    checkScrollPosition,
  }
}

// Mixin para componentes Vue.js (alternativa al composable)
export const infiniteScrollMixin = {
  data() {
    return {
      infiniteScroll: {
        threshold: 200,
        throttleDelay: 100,
        scrollTimeout: null,
      },
    }
  },

  mounted() {
    this.bindInfiniteScrollEvents()
  },

  beforeDestroy() {
    this.unbindInfiniteScrollEvents()
  },

  methods: {
    bindInfiniteScrollEvents() {
      window.addEventListener('scroll', this.handleInfiniteScroll, {
        passive: true,
      })
      window.addEventListener('resize', this.handleInfiniteResize)
    },

    unbindInfiniteScrollEvents() {
      window.removeEventListener('scroll', this.handleInfiniteScroll)
      window.removeEventListener('resize', this.handleInfiniteResize)
      if (this.infiniteScroll.scrollTimeout) {
        clearTimeout(this.infiniteScroll.scrollTimeout)
        this.infiniteScroll.scrollTimeout = null
      }
    },

    handleInfiniteScroll() {
      if (this.infiniteScroll.scrollTimeout) return

      this.infiniteScroll.scrollTimeout = setTimeout(() => {
        this.checkInfiniteScrollPosition()
        this.infiniteScroll.scrollTimeout = null
      }, this.infiniteScroll.throttleDelay)
    },

    checkInfiniteScrollPosition() {
      const scrollHeight = document.documentElement.scrollHeight
      const scrollTop = document.documentElement.scrollTop
      const clientHeight = document.documentElement.clientHeight

      const nearBottom =
        scrollTop + clientHeight >= scrollHeight - this.infiniteScroll.threshold

      if (nearBottom && this.shouldLoadMoreData && this.shouldLoadMoreData()) {
        this.loadMoreData && this.loadMoreData()
      }
    },

    handleInfiniteResize() {
      this.$nextTick(() => {
        this.checkInfiniteScrollPosition()
      })
    },

    // Métodos que deben ser implementados por el componente
    shouldLoadMoreData() {
      console.warn('shouldLoadMoreData method should be implemented')
      return false
    },

    loadMoreData() {
      console.warn('loadMoreData method should be implemented')
    },
  },
}

export default {
  useInfiniteScroll,
  infiniteScrollMixin,
}
