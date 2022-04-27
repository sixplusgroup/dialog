import {axios} from '@/utils/request'

export function get_typical_case_card_base_infos_api() {
  console.log('get_typical_case_card_base_infos_api')
  return axios({
    url: '/case/get_typical_case_card_base_infos',
    method: 'GET'
  })
}

export function get_loudness_api(data) {
  console.log('get_loudness_api')
  console.log(data)
  return axios({
    url: '/case/get_loudness',
    method: 'GET',
    params: data
  })
}

export function get_case_dialogue_list_api(data) {
  console.log('get_case_dialogue_list_api')
  console.log(data)
  return axios({
    url: '/case/get_case_dialogue_list',
    method: 'GET',
    params: data
  })
}

export function get_get_recommendation_point_list_api(data) {
  console.log('get_recommendation_point_list_api')
  console.log(data)
  return axios({
    url: '/case/get_recommendation_point_list',
    method: 'GET',
    params: data
  })
}

export function get_case_evaluation_api(data) {
  console.log('get_case_evaluation_api')
  console.log(data)
  return axios({
    url: '/case/get_case_evaluation',
    method: 'GET',
    params: data
  })
}

export function get_staff_case_card_base_infos_api(staffId) {
  console.log('get_staff_case_card_base_infos_api')
  return axios({
    url: '/case/get_staff_case_card_base_infos',
    method: 'GET',
    params: {staffId: staffId}
  })
}

