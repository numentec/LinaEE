export default async ({ store, redirect, route }) => {
  if (process.client) {
    await store.dispatch('nuxtClientInit', { redirect, route })
  }
}
