
// import {getUserPortraitAPI, getUserBookAPI, cancelBookAPI, wordCloudAPI} from '@/api/userPortrait'

import {message} from 'ant-design-vue'
import {get_staff_case_card_base_infos_api} from "@/api/case";
import {
  get_CSStaff_by_id_api,
  get_staff_evaluation_by_staff_id_api,
  get_get_staff_history_scores_api
} from "@/api/CSStaff";
import {get_staff_history_scores_api} from "../../api/CSStaff";

const recordCase = {
  state: {
    // curCaseCSS: {
    //   staffName:"潜心一致OK爸",
    //   CSSId:"S010",
    //   NumOfCusto:"30",
    //   NumOfCase:"45",
    //   serviceEvaluation:3.5,
    // },
    curCaseCSS: {},
    curSelectedRecord:{}
  },
  mutations: {
    set_curCaseCSS: function (state, data) {
      state.curCaseCSS=data;
    },
    set_curSelectedRecord: function (state, data) {
      console.log("设置了curSelectedRecord")
      console.log(data);
      state.curSelectedRecord=data;
    },
    set_curSelectedRecordEmpty: function (state, data) {
      state.curSelectedRecord={};
    },
    set_CSStaffId: function (state, data) {
      state.curCaseCSS.CSSId=data;
    },
  },
  actions: {

    getCurRecordList: async ({state, commit}, data) => {
      //可以分页处理
      // console.log("进入"+"getCurRecordList");
      // console.log(data);
      const res = await get_staff_case_card_base_infos_api(data)
      // console.log(res)
      if (res) {
        // console.log("获取 当前客服所有案例 成功");
        for(let case_card of res.data){
          case_card.key = case_card.caseName
          case_card.typicalPoint = case_card.date
        }
        return res.data;
      } else {
        console.log("获取 当前客服所有案例 失败")
      }
    },

    getCurCaseCSS: async ({state, commit}, data) => {
      //可以分页处理
      // console.log("进入"+"getCurCaseCSS");
      // console.log(data);
      const res = await get_CSStaff_by_id_api(data)
      console.log(res)
      if (res) {
        // console.log("获取 当前客服 成功")
        commit('set_curCaseCSS',res.data)
        return res.data;
      } else {
        console.log("获取 当前客服 失败")
      }
    },

    getStaffEvaluation: async ({state, commit}) => {
      //可以分页处理
      // console.log("进入"+"getStaffEvaluation");
      const res = await get_staff_evaluation_by_staff_id_api(state.curCaseCSS.CSSId)
      // console.log(res)
      if (res) {
        // console.log("获取 客服评价 成功")
        return res.data;
      } else {
        console.log("获取 客服评价 失败")
      }
    },

    getStaffHistoryScores: async ({state, commit}) => {
      //可以分页处理
      // console.log("进入"+"getStaffHistoryScores");
      const res = await get_staff_history_scores_api(state.curCaseCSS.CSSId)
      // console.log(res)
      if (res) {
        // console.log("获取 客服历史得分 成功")
        return res.data;
      } else {
        console.log("获取 客服历史得分 失败")
      }
    },
  }
};
export default recordCase
