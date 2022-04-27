import Vue from 'vue'
// const Vue = ()=>import('vue')
import VueRouter from 'vue-router'
// const VueRouter = ()=> import( 'vue-router')


// import layout from "../layout";
const layout = ()=> import("../layout")
// import Qs from 'qs';

const homePage =()=>import('../components/homePage')

const recordCasePage = ()=> import("../components/recordCasePage")
const recordCaseAnalysis = ()=> import("../components/recordCaseAnalysis")
const customerServiceEvaluation= ()=> import("../components/customerServiceEvaluation")
const addTemplate = ()=> import("../components/addTemplate")

Vue.use(VueRouter);
const routes = [
  {
    //首页
    path: '/',
    redirect: '/homePage',
  },
  {
    //首页
    path: '/homePage',
    name:'homePage',
    component: homePage,
  },
  //todo 目前的layout作为子层的 挂载父页面 路由不变
  //新增一个 homePage page！！
  {
    path: '/subPage',
    name: 'layout',
    redirect: '/recordCasePage',
    component: layout,
    children: [
      {
        path: '/recordCasePage',
        name: 'recordCasePage',
        component: recordCasePage
      },
      {
        path: '/recordCaseAnalysis',
        name: 'recordCaseAnalysis',
        component: recordCaseAnalysis
      },
      {
        path: '/customerServiceEvaluation',
        name: 'customerServiceEvaluation',
        component: customerServiceEvaluation
      },
      {
        path: '/addTemplate',
        name: 'addTemplate',
        component: addTemplate
      },
    ]
  },

]

const createRouter = () => new VueRouter({
  // mode: 'history',
  scrollBehavior: () => ({y: 0}),
  routes
});

const router = createRouter()



// router.beforeEach((to, from, next) => {
//   // JWT Token
//   if (localStorage.getItem("token")) {
//     if (to.fullPath === '/login') {
//       next('/')
//     }
//     else {
//       next()
//     }
//   } else {
//     // 无Token
//     if (to.fullPath === '/login') {
//       next()
//     } else {
//       next('/login')
//     }
//   }
// });

export function resetRouter() {
  const newRouter = createRouter();
  router.matcher = newRouter.matcher // reset router
}

export default router

import VueAMap from 'vue-amap';

Vue.use(VueAMap);
// 初始化vue-amap

VueAMap.initAMapApiLoader({
  // 高德的key
  key: '6df2e350cf91472c7bcc795cefd719f4',
  // 插件集合
  plugin: ['AMap.Autocomplete', 'AMap.PlaceSearch', 'AMap.Scale', 'AMap.OverView', 'AMap.ToolBar', 'AMap.MapType', 'AMap.PolyEditor', 'AMap.CircleEditor'],
  // 高德 sdk 版本，默认为 1.4.4
  v: '1.4.4'
});
