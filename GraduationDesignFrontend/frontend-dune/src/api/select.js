import {axios} from '@/utils/request'

const api = {
  selectPre: '/api/v3/query'
};

export function changeSelectionAPI(data) {
  return axios({
    url: `${api.selectPre}/series`,
    method: 'post',
    data
  })
}

export function getCarGraphAPI(id) {
  return axios({
    url: `${api.selectPre}/series/graph/${id}`,
    method: 'get',
  })
}
export function getSeriesCarListAPI(id) {
  return axios({
    url: `${api.selectPre}/series/seller/${id}/carInfos`,
    method: 'get',
  })
}
export function getSellerListAPI(data) {
  return axios({
    url: `${api.selectPre}/series/seller/details`,
    method: 'post',
    data
  })
}
export function sentAskingOrderAPI(data) {
  return axios({
    url: `${api.selectPre}/series/seller/query_price`,
    method: 'post',
    data
  })
}


