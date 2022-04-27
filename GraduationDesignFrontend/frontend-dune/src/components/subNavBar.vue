<template>
  <div class="navBarContainer">
    <div style="width: 100%; height: 100%" >
      <a-menu
        :default-selected-keys="['0']"
        v-model="current"
        mode="inline"
        theme="dark"
        :inline-collapsed="collapsed"
      >
        <a-menu-item v-if="!collapsed"  @click="jumpToHome" style="font-size: 20px;color: #FFFFFF;margin-bottom: 20px;margin-top: 20px">
          语音情绪分析
        </a-menu-item>
        <a-menu-item v-if="collapsed"  @click="jumpToHome" style="color: #FFFFFF;margin-bottom: 20px;margin-top: 20px;">
          <a-icon type="slack" :style="{ fontSize: '24px',color:'#FFFFFF'}"/>
          <span>语音情绪分析</span>
        </a-menu-item>
        <a-menu-item key="0"  @click="toggleCollapsed">
          <a-icon :type="collapsed ? 'menu-unfold' : 'menu-fold'" />
          <span>收起</span>
        </a-menu-item>

        <a-menu-item  @click="jumpToRCPage" key="1">
          <a-icon type="pie-chart" />
          <span>客服案例</span>
        </a-menu-item>
        <a-menu-item  @click="jumpToRCAna" key="2">
          <a-icon type="desktop" />
          <span>案例分析</span>
        </a-menu-item>
        <a-menu-item  @click="jumpToCSEva" key="3">
        <a-icon type="desktop" />
        <span>客服评价</span>
      </a-menu-item>
        <a-menu-item  @click="jumpToADTem" key="4">
          <a-icon type="form" />
          <span>添加模板</span>
        </a-menu-item>
      </a-menu>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from 'vuex'
export default {
  name: "subNavBar",
  data() {
    return {
      collapsed: false,
      current: ['1'],
    };
  },
  watch: {
    //监听路由，只要路由有变化(路径，参数等变化)都有执行下面的函数，你可以
    $route: {
      handler: function (val, oldVal) {
        // let _urlParams = this.$route.params;
        // //created事件触发的函数可以在这里写...
        // //都是componentA组件，声明周期还在，改变不了
        // console.log("上面")
        console.log('改变了')
        console.log(this.$route.name);

        if (this.$route.name == 'recordCasePage' ) {
          console.log("当前页面改变成为 recordCasePage");
          this.current = ['1']
        } else if (this.$route.name == 'recordCaseAnalysis') {
          console.log("当前页面改变成为 recordCaseAnalysis");
          this.current = ['2']
        }
      },
      deep: true
    }
  },
  computed: {
    ...mapGetters([
      'curSelectedRecord',
    ])
  },
  mounted() {
    // this.drawerTitle = "询底价: " + this.car.name;
    // if (this.userId === -1) await this.getUserInfo();
    // console.log("subBar挂载");
    // console.log(this.curSelectedRecord);
    let curTag=Object.keys(this.curSelectedRecord).length === 0?['1']:['2'];
    // console.log(curTag);
    this.current= curTag;
  },
  methods: {
    ...mapMutations([
      'set_curCaseCSS',
      'set_curSelectedRecord'
    ]),
    jumpToHome(){

      console.log("点击 jumpToHome");
      // todo 清空当前的所有 信息
      this.set_curCaseCSS({});
      this.set_curSelectedRecord({});
      this.$router.push("/homePage")
    },
    jumpToRCPage(){
      console.log("点击 jumpToRCPage");
      this.$router.push("/recordCasePage");
    },
    jumpToRCAna(){
      console.log("点击 jumpToRCAna");
      this.$router.push("/recordCaseAnalysis");
    },
    jumpToCSEva(){
      console.log("点击 jumpToRCAna");
      this.$router.push("/customerServiceEvaluation");
    },
    jumpToADTem(){
      console.log("点击 jumpToADTem");
      this.$router.push("/addTemplate");
    },
    sleep(time){
      return new Promise(resolve => {
        setTimeout(resolve,time)
      })
    },
    toggleCollapsed() {

      this.sleep(10000).then(res =>{
        console.log("刷新完毕");
      })
      this.collapsed = !this.collapsed;
    },
  },
}
</script>

<style scoped>
.ant-menu-inline{
  height: 100%;
}
.ant-menu-inline-collapsed{
  height: 100%;
}
.ant-menu-item{
  color: #A5AEB3;
}
</style>
