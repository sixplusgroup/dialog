// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import store from './store'

import App from './App'
import router from './router'
import 'ant-design-vue/dist/antd.css';
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.less'


Vue.config.productionTip = false

Vue.use(Antd);
//
import * as echarts from 'echarts';
Vue.prototype.$echarts = echarts

import { Lazyload } from 'vant' // 导入懒加载模块Lazyload
Vue.use(Lazyload) // 注册懒加载指令



import infiniteScroll from "vue-infinite-scroll";
Vue.use(infiniteScroll);


// router.beforeEach((to, from, next) => {
//
//   //获取用户登录成功后储存的登录标志
//   let getFlag = localStorage.getItem("Flag");
//
//   //如果登录标志存在且为isLogin，即用户已登录
//   if(getFlag === "isLogin"){
//
//     //设置vuex登录状态为已登录
//     store.state.isLogin = true;
//     next();
//
//     //如果已登录，还想想进入登录注册界面，则定向回首页
//     if (!to.meta.isLogin) {
//       //iViewUi友好提示
//       // iView.Message.error('请先退出登录')
//       next({
//         path: '/homePage'
//       })
//     }
//
//     //如果登录标志不存在，即未登录
//   }else{
//
//     //用户想进入需要登录的页面，则定向回登录界面
//     if(to.meta.isLogin){
//       next({
//         path: '/login',
//       })
//     }else{
//       next()
//     }
//
//   }
//
// });

router.afterEach(route => {
  window.scroll(0, 0);
});

new Vue({
  router,//引入router
  store,//引vuex
  render: h => h(App)
}).$mount('#app');
//挂在到app,进行渲染
