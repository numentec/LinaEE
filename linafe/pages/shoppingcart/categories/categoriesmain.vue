<template>
  <div class="shopping-cart mt-4">
    <div v-for="(item, index) in filteredItems" :key="index">
      <CategoryCard :category="item" />
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import CategoryCard from '~/components/shoppingcart/CategoryCard.vue'

const BRANDSDATA = ['Brand 1', 'Brand 2', 'Brand 3', 'Brand 4', 'Brand 5']

function getRandomSubarray(arr, size) {
  const shuffled = arr.slice(0)
  let i = arr.length
  let temp, index
  while (i--) {
    index = Math.floor((i + 1) * Math.random())
    temp = shuffled[index]
    shuffled[index] = shuffled[i]
    shuffled[i] = temp
  }
  return shuffled.slice(0, size)
}

function makeItems(images) {
  const items = []
  for (let i = 0; i < 100; i++) {
    items.push({
      image: images[Math.floor(Math.random() * images.length)],
      name: `Category ${i}`,
      price: Math.floor(Math.random() * 1000),
      description: `Description for Category ${i}`,
      instock: Math.floor(Math.random() * 100),
      brands: getRandomSubarray(BRANDSDATA, 3),
      link: '/shoppingcart/categories/categoriessub',
    })
  }

  return new Promise((resolve) => {
    resolve({ data: items })
  })
}

export default {
  components: {
    CategoryCard,
  },
  async asyncData({ error }) {
    try {
      const images = [
        'http://192.168.1.55:8001/media/images/bifavoritos/prev3.gif',
        '/shoppingcart/H23100256A.jpg',
        '/shoppingcart/H23100133A.jpg',
        '/shoppingcart/H22200482A.jpg',
        '/shoppingcart/W231013199.jpg',
        '/shoppingcart/W231013210.jpg',
        '/shoppingcart/HBS01401N-B.jpg',
        '/shoppingcart/VLCSMLORG.jpg',
      ]

      const { data } = await makeItems(images)

      return {
        items: data,
      }
    } catch (err) {
      if (err.response) {
        error({
          statusCode: err.response.status,
          message: err.response.data.detail,
        })
      } else {
        error({
          statusCode: 503,
          message: 'No se pudo cargar la lista. Intente luego',
        })
      }
    }
  },

  data() {
    return {
      items: [],
      brands: ['Brand 1', 'Brand 2', 'Brand 3', 'Brand 4', 'Brand 5'],
    }
  },

  computed: {
    ...mapGetters('shoppingcart/categories', [
      'getSelectedBrands',
      'getSearchCategory',
    ]),
    filteredItems() {
      return this.items.filter((item) => {
        const selectedBrands = this.getSelectedBrands
        let searchCategory = this.getSearchCategory

        if (searchCategory === null || searchCategory === undefined) {
          searchCategory = ''
        }

        if (searchCategory === '' && selectedBrands.length === 0) {
          return true
        }

        if (selectedBrands.length > 0) {
          return (
            item.name.toLowerCase().includes(searchCategory.toLowerCase()) &&
            selectedBrands.includes(item.brands[0])
          )
        }

        return item.name.toLowerCase().includes(searchCategory.toLowerCase())
      })
    },
  },
  mounted() {
    window.scrollTo(0, 0)
  },
}
</script>

<style scoped>
.shopping-cart {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
</style>
