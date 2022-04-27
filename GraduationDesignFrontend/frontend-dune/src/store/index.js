import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters'

// import homePage from "./modules/homePage";

// const CSStaff =()=>import("./modules/CSStaff")

// const select =()=>import("./modules/select")


// const userPortrait =()=>import("./modules/userPortrait")
// const recommend =()=>import("./modules/recommend")
import recordCase from "./modules/recordCase"
import caseDisplay from "./modules/caseDisplay"
import homePage from "./modules/homePage";
Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    caseDisplay,
    homePage,
    recordCase
  },
  // state: {
  //   isLogin: false,
  // },
  mutations: {
    //保存登录状态
    // userStatus(state, flag) {
    //   state.isLogin = flag
    // },
  },
  actions: {
    //获取登录状态
    // userLogin({commit}, flag) {
    //   commit("userStatus", flag)
    // },
  },
  getters
})

