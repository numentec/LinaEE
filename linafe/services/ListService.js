import axios from 'axios'

const apiClient = axios.create({
  baseURL: process.env.API_URL_SERVER,
  withCredentials: false, // This is the default
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
})

export default {
  getList(apipath) {
    return apiClient.get(apipath)
  },
}
