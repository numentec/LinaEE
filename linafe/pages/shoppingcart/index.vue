<template>
  <div class="shopping-cart">
    <div v-for="(item, index) in items" :key="index">
      <ShopCard :product="item" />
    </div>
  </div>
</template>

<script>
import ShopCard from '~/components/shoppingcart/ShopCard.vue'

function makeItems(images) {
  const items = []
  for (let i = 0; i < 100; i++) {
    items.push({
      image: images[Math.floor(Math.random() * images.length)],
      name: `Product ${i}`,
      price: 100.0,
      description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
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
        'http://192.168.1.55:8001/media/images/bifavoritos/prev1.jpg',
        'http://192.168.1.55:8001/media/images/bifavoritos/prev2.png',
        'http://192.168.1.55:8001/media/images/bifavoritos/prev3.gif',
        'http://192.168.1.55:8001/media/images/bifavoritos/rpt01.jpeg',
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
    }
  },
  // mounted() {
  //   // const images = ['/uc1.jpg', '/uc2.jpg', '/uc3.jpg', '/uc4.jpg']
  //   const images = [
  //     'http://192.168.1.55:8001/media/images/bifavoritos/prev1.jpg',
  //     'http://192.168.1.55:8001/media/images/bifavoritos/prev2.png',
  //     'http://192.168.1.55:8001/media/images/bifavoritos/prev3.gif',
  //     'http://192.168.1.55:8001/media/images/bifavoritos/rpt01.jpeg',
  //   ]
  //   for (let i = 0; i < 100; i++) {
  //     this.items.push({
  //       image: images[Math.floor(Math.random() * images.length)],
  //     })
  //   }
  // },
}
</script>

<style scoped>
.shopping-cart {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
</style>
