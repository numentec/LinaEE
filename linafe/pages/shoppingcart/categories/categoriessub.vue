<template>
  <div class="shopping-cart mt-4">
    <div v-for="(item, index) in filteredItems" :key="index">
      <ShopCard :category="item" />
    </div>
  </div>
</template>

<script>
import ShopCard from '~/components/shoppingcart/ShopCard.vue'

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
      name: `Sub Category ${i}`,
      price: 100.0,
      description: `Description for Sub Category ${i}`,
      brands: getRandomSubarray(BRANDSDATA, 3),
    })
  }

  return new Promise((resolve) => {
    resolve({ data: items })
  })
}

export default {
  components: {
    ShopCard,
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

  inject: ['selected_brands', 'search_subcategory'],

  data() {
    return {
      items: [],
      brands: ['Brand 1', 'Brand 2', 'Brand 3', 'Brand 4', 'Brand 5'],
    }
  },

  computed: {
    filteredItems() {
      return this.items.filter((item) => {
        if (this.search_subcategory === null) {
          this.search_subcategory = ''
        }
        if (
          this.search_subcategory === '' &&
          this.selected_brands.length === 0
        ) {
          return true
        }
        if (this.selected_brands.length > 0) {
          return (
            item.name
              .toLowerCase()
              .includes(this.search_subcategory.toLowerCase()) &&
            this.selected_brands.includes(item.brands[0])
          )
        }
        return item.name
          .toLowerCase()
          .includes(this.search_subcategory.toLowerCase())
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
