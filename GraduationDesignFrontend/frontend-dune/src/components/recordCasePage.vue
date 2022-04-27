<template>
  <div class="recordPageContainer">
    <div class="subBreadcrumb">
      <div class="RecordTitle">
        <a @click="goBackHome" class="title" style="height: 25px">我的工作台</a>
        <div class="breadBar" style="height: 25px;margin-left: 15px">
          <a-breadcrumb>
            <a-breadcrumb-item href="">
              <a-icon type="homePage" />
            </a-breadcrumb-item>
            <a-breadcrumb-item href="">
              <a-icon type="customer-service" />
              <span>客服</span>
            </a-breadcrumb-item>
            <a-breadcrumb-item>
              客服案例
            </a-breadcrumb-item>
          </a-breadcrumb>
        </div>
      </div>
<!--      todo 可以添加 客服头像和名字。。-->
      <div class="CSSInfo">
        <div class="CSSName">{{this.curCaseCSS.staffName}}</div>
        <div class="CSSName">{{this.curCaseCSS.CSSId}}</div>
      </div>

    </div>
    <div class="recordPageContent">
      <div class="recordPageHeader">
        <div class="headerTitle" style="font-size: 18px;font-weight:normal;margin-left: 5px">所有案例</div>
        <a-icon type="sync" :spin="isRecordSync"   :style="{ fontSize: '20px',color:'#727275'}" @click="this.toSyncRecord" style="margin-right: 20px"/>
      </div>
      <div class="recordPageHolder" >
        <record-card  :recordBaseInfo="item" :key="item.key" v-for="item in RecordList"></record-card>
      </div>

      <div style="width: 100%;text-align: center;margin-top: 70px">
        <a-pagination size="small" :total="allRecordNum"
                      :page-size="6"
                      :current="recordCurrentPage"
                      @change="onRecordPageChange"
        />
      </div>
    </div>
  </div>
</template>

<script>

import recordCard from "./recordCard";
import {mapActions, mapGetters} from "vuex";

export default {
  name: "recordCasePage",
  components: { recordCard},
  data() {
    return {
      isRecordSync:false,
      allRecordList:[],
      allRecordNum:0,
      recordCurrentPage:1,
      RecordList:[],
    }
  },
  computed: {
    ...mapGetters([
      'curCaseCSS'
    ]),
  },
  async mounted() {

    console.log("进入 客服案例页");
    console.log(this.curCaseCSS);

    await this.getRecordList();

  },
  methods: {
    ...mapActions([
      'getCurRecordList',
    ]),

    async getRecordList(){
      let curRecordList = await this.getCurRecordList(this.curCaseCSS.CSSId)
      this.allRecordList = curRecordList
      this.allRecordNum = curRecordList.length
      this.RecordList = []
      for(let i=0;i<Math.min(6,curRecordList.length);i++)
        this.RecordList.push(curRecordList[i])
    },

    goBackHome(){
      this.$router.push("/homepage")
    },
    onRecordPageChange(current) {
      console.log(current);
      this.recordCurrentPage = current
      this.RecordList = []
      for(let i = 6*(current-1);i<Math.min(6*current,this.allRecordNum);i++){
        this.RecordList.push(this.allRecordList[i])
      }
    },
    sleep(time){
      return new Promise(resolve => {
        setTimeout(resolve,time)
      })
    },
    async toSyncRecord(){
      this.isRecordSync = !this.isRecordSync;
      await this.getRecordList()
      this.recordCurrentPage = 1
      this.isRecordSync = !this.isRecordSync;
    }
  }
}
</script>

<style scoped>
.recordPageContainer{

  width: 100%;
  height: 100%;
  background-color:#f8f8f8;
}
.subBreadcrumb{
  padding-left: 11vw;
  width: 100%;
  height: 6vh;
  display: flex;
  align-content: center;
  justify-content: space-between;
  background-color: #FFFFFF;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
.RecordTitle{
  margin-top: 15px;
  display: flex;
  align-content: center;
}
.recordPageContent{
  padding-left: 10vw;
  width: 100%;
  height: 94vh;
}
.recordPageHeader{
  padding-top: 20px;
  padding-left: 20px;
  padding-bottom: 20px;
  width: 100%;
  height: 10vh;
  display: flex;
  align-content: center;
  justify-content: space-between;
}
.recordPageHolder{
  padding-left: 9vw;
  width: 85%;
  height: 64vh;
  display: grid;
  grid-template-columns:  33% 33% 33%;
  grid-template-rows: 40% 40%;
  grid-gap: 20px 20px;
  justify-items:center;
  align-items:center;
}


</style>
