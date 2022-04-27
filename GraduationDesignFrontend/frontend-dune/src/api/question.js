import {axios} from '@/utils/request'

const api = {
  qPre: '/api/v3/question'
};

export function questionAPI(data) {
  return axios({
    url: `${api.qPre}`,
    method: 'post',
    data
  })
}


// export function getRecommendCarListByUserIdAPI(data) {
//   return axios({
//     url: `${api.recommendPre}/getRecommendCars/${data}`,
//     method: 'get'
//   })
// }
