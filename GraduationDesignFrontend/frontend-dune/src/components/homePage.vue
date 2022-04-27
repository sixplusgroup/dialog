<template>
  <div id="root">
<!--    <Header class="outHeaderStyle"></Header>-->
    <div class="mainContainer">
      <div class="recordPanel">
        <div class="recordHeader">
          <div class="headerTitle" style="font-size: 18px;font-weight:normal;margin-left: 5px">典型案例</div>
        </div>
        <div class="recordHolder" >
          <record-card :recordBaseInfo="item" :key="item.key" v-for="item in TypicalRecordList">
          </record-card>
        </div>
        <div style="width: 100%;text-align: center">
          <a-pagination size="small" :total="12"
                        page-size.sync="6"
                        :current="caseCurrentPage"
                        @change="onRecordPageChange"
          />
        </div>
      </div>

      <div class="staffPanel">
        <div class="staffHeader">
          <div class="headerTitle" style="font-size: 18px;font-weight: normal;margin-left: 5px">客服成员</div>
          <div>
            <a-button type="primary" size="small" style="margin-right: 20px" icon="user-add" @click="this.showUpload">
              添加客服
            </a-button>
          </div>

        </div>
        <div class="staffHolder" >
          <c-s-s-card style="margin-bottom: 40px" :CSStaffBaseInfo="item" :key="item.CSSId"  v-for="item in staffList"></c-s-s-card>
        </div>
        <div style="width: 100%;text-align: center">
          <a-pagination  :total="allStaffNum"
                        :page-size="9"
                        :current="staffCurrentPage"
                        @change="onStaffPageChange"
          />
        </div>
      </div>
    </div>
    <a-modal
      title="添加新客服"
      :visible="this.visible"
      @ok="handleOk"
      @cancel="handleCancel"
    >
      <a-input ref="userNameInput" v-model="addStaffName" placeholder="客服名" style="margin-bottom: 10px">
        <a-icon slot="prefix" type="user" />
        <a-tooltip slot="suffix" title="客服的名字">
          <a-icon type="info-circle" style="color: rgba(0,0,0,.45)" />
        </a-tooltip>
      </a-input>
      <a-upload-dragger
        :file-list="fileList"
        :multiple="false"
        :before-upload="beforeUpload"
        :remove="handleRemove"
      >
        <p class="ant-upload-drag-icon">
          <a-icon type="inbox" />
        </p>
        <p class="ant-upload-text">
          Click or drag file to this area to upload
        </p>
        <p class="ant-upload-hint">
          Support for a single or bulk upload. Strictly prohibit from uploading company data or other
          band files
        </p>
      </a-upload-dragger>
    </a-modal>
  </div>
</template>
<script>
// import Bg from '../assets/zyb2.jpg'
import {RecycleScroller} from "vue-virtual-scroller";
import {mapActions, mapGetters, mapMutations} from 'vuex'
import Header from './header.vue'
import recordCard from "./recordCard";
import CSSCard from "./CSSCard";
import {add_staff_api} from "@/api/CSStaff";
//引图片方式
const Bg=()=>import('../assets/zyb2.jpg')
// const radarEvaluate=()=>import("./radarEvaluate");

export default {
  name: "homePage",
  components: { Header,recordCard,CSSCard},
  data() {
    return {
      caseCurrentPage: 1,
      staffCurrentPage: 1,
      visible:false,
      bg: Bg,
      question:"",
      isRecordSync:false,
      allTypicalRecords:[],
      TypicalRecordList:[],
      allStaffs:[],
      allStaffNum:0,
      staffList:[],
      fileList: [],
      addStaffName: '',
      paginationOpt: {

      }
    }
  },
  computed: {
    ...mapGetters([
      'userId'
    ]),
  },
  async mounted() {
    await this.getBaseDisplayData();
  },

  methods: {
    ...mapActions([
      'getAllCSStaff',
      'getTypicalRecords',
    ]),
    showUpload(){
      this.visible=true;
    },
    async handleOk(){
      console.log('handleOk')
      console.log(this.fileList)
      if(this.fileList.length>0){
        console.log('上传')
        const formData = new FormData()
        formData.append('name',this.addStaffName)
        formData.append('file',this.fileList[0])
        let res = await add_staff_api(formData)
        console.log(res)
        if(res){
          let status = res.code
          if (status === 200) {
            this.$message.success(`添加客服成功`);
            await this.getBaseDisplayData()
            this.caseCurrentPage = 1
            this.staffCurrentPage = 1
          } else {
            this.$message.error(`添加客服失败 ${res.message}`);
          }
        }
      }
      this.fileList = []
      this.addStaffName = ''
      this.visible=false;
    },
    handleCancel(){
      this.visible=false;
    },
    handleRemove (file) {
      console.log('remove file')
      let index = this.fileList.indexOf(file)
      console.log(index)
      let newFileList = this.fileList.slice()
      newFileList.splice(index, 1)
      this.fileList = newFileList
    },
    beforeUpload (file) {
      this.fileList = [...this.fileList, file]
      console.log(this.fileList)
      return false
    },
    async getBaseDisplayData() {
      let typicalRecords=await this.getTypicalRecords();
      this.allTypicalRecords = typicalRecords
      console.log(typicalRecords)
      this.TypicalRecordList = []
      for(let i=0;i<Math.min(6,typicalRecords.length) ;i++){
        this.TypicalRecordList.push(typicalRecords[i])
      }
      let staffList=await this.getAllCSStaff();
      this.allStaffs = staffList
      this.allStaffNum = staffList.length
      console.log(this.allStaffNum)
      this.staffList = []
      for(let i=0;i<Math.min(9,staffList.length);i++){
        this.staffList.push(staffList[i])
      }
    },
    onStaffPageChange(current) {
      console.log(current);
      this.staffCurrentPage = current
      this.staffList = []
      for(let i = 9*(current-1);i<Math.min(9*current,this.allStaffNum);i++){
        this.staffList.push(this.allStaffs[i])
      }
    },
    onRecordPageChange(current) {
      console.log(current);
      this.caseCurrentPage = current
      this.TypicalRecordList = []
      for(let i = 6*(current-1);i<6*current;i++){
        this.TypicalRecordList.push(this.allTypicalRecords[i])
      }
    },
  }

}
</script>

<style scoped>
/*#root {*/
/*  text-align: center;*/
/*  //padding-top: 10em;*/
/*  //background-image: url('../assets/zyb2.jpg');*/
/*  //background-repeat: no-repeat;*/
/*  background-color: #f8f8f8;*/
/*  !*overflow: hidden;*!*/
/*  !*background-size: cover;*!*/
/*  width: 100%;*/
/*  height: 100%;*/
/*  position: fixed;*/
/*  background-position: 0px 0px;*/
/*  background-size: 100% 100%;*/
/*}*/
.mainContainer{
  margin-top: 3px;
  //padding-top: 20px;
  //padding-left: 20px;
  padding-top: 5px;
  padding-bottom: 20px;
  width: 100%;
  height: 100%;
  background-color: #F9F9F9;
}
.recordHeader{
  width: 100%;
  height: 8vh;
  display: flex;
  align-content: center;
  justify-content: space-between;
}
.recordPanel{
  width: 80%;
  height: 60vh;
  margin-left: 10%;
  background-color: #FFFFFF;
  border-radius: 2px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  padding: 20px 20px;
}

.recordHolder{
  width: 100%;
  display: grid;
  grid-template-columns:  32% 32% 32%;
  grid-template-rows: 45% 45%;
  grid-gap: 20px 20px;
  justify-items:center;
  align-items:center;
}
.staffHolder{
  margin-bottom: 30px;
  width: 100%;
  height: 80%;
  display: grid;
  grid-template-columns:  32% 32% 32%;
  grid-template-rows: 22% 22%  22%  ;
  grid-gap: 20px 20px;
  justify-items:center;
  align-items:center;
}
.staffPanel{
  margin-top: 20px;
  width: 80%;
  height:  75vh;
  margin-left: 10%;
  background-color: #FFFFFF;
  border-radius: 2px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  padding: 20px 20px;
}

.staffHeader{
  width: 100%;
  height: 8vh;
  display: flex;
  align-content: center;
  justify-content: space-between;
}
.outHeaderStyle{
  position:fixed;
  top:0px;
  width: 100vw;
  z-index:999;
}


</style>

