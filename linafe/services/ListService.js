import axios from 'axios'

const apiClient = axios.create({
  baseURL: `http://192.168.15.4:8001/linapi`,
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
