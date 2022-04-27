<template>
  <div id="layout">
<!--todo  作为子页面的 路由，，初步使用左右方式进行排版，需要将二者进行左右布局，-->
<!-- todo 直接重写左侧栏即可-->
<!--    <Header class="outHeaderStyle"></Header>-->
    <sub-nav-bar class="navBarStyle"></sub-nav-bar>
    <transition name="fade-transform" mode="out-in">
      <router-view class="subPageStyle"/>
    </transition>
    <!--        <footerPage/>-->
  </div>
</template>
<script>
  import Header from './components/header.vue'
  import subNavBar from "./components/subNavBar";

  export default {
    name: 'layout',
    components: {Header,subNavBar},
  }
</script>
<style>
  #layout {
    /*height: 95vh;*/
    display: flex;
    width: 100%;
    height: 100%;
  }
  .navBarStyle{
    position:fixed;
    top:0px;
    z-index:999;

    width: 10vw;
    height: 100vh;
    background-color: transparent;
  }
  .subPageStyle{
    float: right;
    width: 100vw;
    height: 100vh;
  }

  .fade-transform-enter-active {
    transition: all .3s ease;
  }

  .fade-transform-enter, .fade-transform-leave-to {
    transform: translateX(20px);
    opacity: 0;
  }
</style>
