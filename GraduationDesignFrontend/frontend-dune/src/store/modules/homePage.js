import {get_typical_case_card_base_infos_api} from '@/api/case';
import {getAllCSStaffAPI} from '@/api/CSStaff';


const homePage = {
  state: {
  },
  mutations: {

  },
  actions: {
    getAllCSStaff: async ({state, commit}) => {
      let res = await getAllCSStaffAPI();
      // console.log(res)
      if (res) {
        // console.log("获取所有客服 成功");
        return res.data;
      } else {
        console.log("获取客服 失败")
      }
    },
    //获取典型的案例
    getTypicalRecords: async ({state, commit}) => {
      //可以分页处理
      let res = await get_typical_case_card_base_infos_api();
      // console.log(res)
      if (res) {
        res = res.data
        for(let case_card of res){
          case_card.key = case_card.caseName+case_card.typicalPoint
        }
        // console.log("获取分页 首页典型案例 成功");
        return res;
      } else {
        console.log("获取 首页典型案例 失败")
      }
    },
  }
}
export default homePage
