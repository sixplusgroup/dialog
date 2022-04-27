import {axios} from '@/utils/request'

const api = {
  staffPre: '/staff'
};

export function loginAPI(data) {
  return axios({
    url:`/login`,
    // url:`/api/CSStaff/login`,
    method: 'POST',
    data
  }).catch((r) => {
    console.log("catch: ", r)
  })
}

export function logoutAPI(data) {
  return axios({
    url:`/logout`,
    method: 'POST',
    data
  }).catch((r) => {
    console.log("catch: ", r)
  })
}


export function registerAPI(data) {
  console.log(data)
  return axios({

    url: `${api.staffPre}/register/individual`,
    method: 'POST',
    data
  })
}

export function getUserInfoAPI(id) {
  return axios({
    url: `${api.staffPre}/${id}/userInfo`,
    method: 'GET'
  });
}

export function updateUserInfoAPI(data) {
  return axios({
    url: `${api.staffPre}/${data.id}/userInfo/update`,
    method: 'POST',
    data
  })
}

export function getuserpicAPI(id) {
  return axios({
    url: `${api.staffPre}/${id}/userInfo/pic`,
    method: 'GET'
  })
}

export function getAllCSStaffAPI(){
  console.log('getAllCSStaffAPI')
  return axios({
    url: `${api.staffPre}/get_all_CSStaff`,
    method: 'GET'
  })
}

export function change_staff_voice_print_api(data){
  console.log("change_staff_voice_print_api")
  return axios({
    url: `${api.staffPre}/change_staff_voice_print`,
    method: 'POST',
    data
  })
}

export function add_staff_api(data){
  console.log("add_staff")
  return axios({
    url: `${api.staffPre}/add_staff`,
    method: 'POST',
    data
  })
}

export function get_CSStaff_by_id_api(staffId){
  console.log("get_CSStaff_by_id_api")
  return axios({
    url: `${api.staffPre}/get_CSStaff_by_id`,
    method: 'GET',
    params: {staffId: staffId}
  })
}

export function get_staff_evaluation_by_staff_id_api(staffId){
  console.log("get_staff_evaluation_by_staff_id_api")
  return axios({
    url: `${api.staffPre}/get_staff_evaluation_by_staff_id`,
    method: 'GET',
    params: {staffId: staffId}
  })
}


export function get_staff_history_scores_api(staffId){
  console.log("get_staff_history_scores_api")
  return axios({
    url: `${api.staffPre}/get_staff_history_scores`,
    method: 'GET',
    params: {staffId: staffId}
  })
}

export function add_template(data){
  console.log("add_template")
  return axios({
    url: `${api.staffPre}/add_template`,
    method: 'POST',
    data
  })
}
