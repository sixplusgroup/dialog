import {axios} from '@/utils/request'

const api = {
  portraitPre: '/api/v3/userPortrait'
};

export function getUserPortraitAPI(id) {
  return axios({
    url: `${api.portraitPre}/${id}`,
    method: 'GET'
  })
}

export function getUserBookAPI(userId) {
  return axios({
    url: `/api/v3/userBehavior/${userId}/2`,
    method: 'GET'
  })
}

export function cancelBookAPI(data) {
  return axios({
    url: `api/v3/userBehavior/${data.userId}/${data.carId}/2`,
    method: 'DELETE'
  })
}

// /api/v3/userPortrait/wordCloud/{userId}

export function wordCloudAPI(userId) {
  console.log("asdfghjk")
  return axios({
    url: `/api/v3/userPortrait/wordCloud/${userId}`,
    method: 'GET'
  })
}
