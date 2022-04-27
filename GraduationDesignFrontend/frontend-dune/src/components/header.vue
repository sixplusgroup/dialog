<template>
  <div>
    <div class="header">
      <div class="mytitle">
        <img class="myLogo" src="../assets/Autopia.png">
      </div>

      <a-menu
          :default-selected-keys="[$route.path]"
          @click="routeLink"
          mode="horizontal"
          style="background-color: transparent;color: rgba(0, 0, 0, 0.71);font-weight: bolder"
          class="menu-top">
          <a-menu-item class="menu-top-item" key="/homePage" >
            <a-icon type="desktop"/>
            <span>语音情绪分析</span>
          </a-menu-item>
          <a-menu-item class="menu-top-item" key="/recommend">
            <a-icon type="appstore" />
            <span>客服文本分析</span>
          </a-menu-item>
          <a-menu-item class="menu-top-item" key="/selectCar">
            <a-icon type="car"/>
            <span>服务案例</span>
          </a-menu-item>

        <a-menu-item class="menu-top-item" key="/question" id="q">
          <a-icon type="question-circle"/>
          <span>客服评价</span>
        </a-menu-item>
        <a-menu-item class="menu-top-item" key="/userPortrait">
          <a-icon type="CSStaff"/>
          <span>客服管理</span>
        </a-menu-item>
      </a-menu>

      <a-dropdown class="userinfo" placement="bottomCenter">
        <div id="user">{{"admin"}}</div>
        <a-menu slot="overlay">
          <a-menu-item key="2">
            退出登录
          </a-menu-item>
        </a-menu>
      </a-dropdown>

    </div>
  </div>
</template>

<script>
  import {mapGetters, mapMutations, mapActions} from 'vuex'

  export default {
    data() {
      return {}
    },
    computed: {
      ...mapGetters([

        'userId',
        'chatMessages'
      ]),

    },
    async mounted(){

    },
    methods: {
      ...mapActions([
        'logout',
      ]),
      ...mapMutations([
        'set_message',
      ]),
      routeLink(e) {
        this.$router.push(e.key)
      },

    }
  }


</script>

<style>
  .menu-top{
    width: 740px;
    height: inherit;
    display: inline-block;
    margin-left: -7em;
    //传递背景颜色
    //background-color: transparent;
    background-color: #FFFFFF;
  }
  .menu-top-item{
    height: inherit
    /*background-color: #01111f;*/
  }

  .header {
    display: flex;
    background-color: #FFFFFF;
    line-height: 45px;
    height: 56px;
    align-items: center;
    justify-content: space-between;
    min-width: 100%;
    /*box-shadow: 0 1px 1px rgba(0, 0, 0, .2);*/
    margin-bottom: 1px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }
  .mytitle {
    font-size: 26px;
    margin: 0 0 0 0;
    color:white;
    //background-color:  rgba(0, 0, 0, 0.71);
    float: left;
  }

  /*.ant-menu.ant-menu-dark .ant-menu-item-selected {*/
  /*  color: #a51f1f;*/
  /*}*/
  #user:hover{
    color: rgba(0, 0, 0, 0.71);
    background-color: transparent;
  }


  .ant-dropdown-menu-item-active{
    color: white;
  }

.userinfo{
  width: 200px;
}
  .myLogo {
    height: 55px;
    width: 200px;
    //控制 颜色反转
    //filter:Invert();
    margin-top: 5px;
  }
  #user{
    float:right;
    margin-bottom: 8px;
    margin-right: 4em;
    width: 2em;
    height:2em;
    color: rgba(0, 0, 0, 0.71);
    font-size: medium;
    font-weight: 500;
    padding-top: 2px;
  }
</style>
