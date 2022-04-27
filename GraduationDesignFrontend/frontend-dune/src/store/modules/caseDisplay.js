import {
  get_loudness_api,
  get_case_dialogue_list_api,
  get_get_recommendation_point_list_api,
  get_case_evaluation_api
} from '@/api/case'


const caseDisplay = {
  state: {
    chatMessages: [],
  },
  mutations: {
    set_message: (state, data) => {
      state.chatMessages = data
    },
  },
  actions: {
    getLoudness: async ({state, commit}, data) =>{
      console.log("获取案例响度"+data.caseName)
      let res = await get_loudness_api(data)
      console.log(res)
      if (res) {
        // console.log("获取案例响度成功");
        return res.data;
      } else {
        console.log("获取案例响度失败")
      }
    },

    getCaseDialogueList: async ({state, commit}, data) =>{
      // console.log("获取案例对话"+data.caseName)
      let res = await get_case_dialogue_list_api(data)
      // console.log(res)
      if (res) {
        // console.log("获取案例对话成功");
        return res.data;
      } else {
        console.log("获取案例对话失败")
      }
    },

    getRecommendationPointList: async ({state, commit}, data) =>{
      // console.log("获取案例推荐"+data.caseName)
      let res = await get_get_recommendation_point_list_api(data)
      // console.log(res)
      if (res) {
        // console.log("获取案例推荐成功");
        return res.data;
      } else {
        console.log("获取案例推荐失败")
      }
    },

    getCaseEvaluation: async ({state, commit}, data) =>{
      // console.log("获取案例评价"+data.caseName)
      let res = await get_case_evaluation_api(data)
      // console.log(res)
      if (res) {
        // console.log("获取案例评价成功");
        return res.data;
      } else {
        console.log("获取案例评价失败")
      }
    }
  }
}
export default caseDisplay
