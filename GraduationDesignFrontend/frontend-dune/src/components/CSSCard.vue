<template>
  <div class="CSSCard-container" >
    <div class="Info-container">
      <img class="imgHolder" @click="jumpToRCP" :src="customerServiceAvatar">
      <div class="CSSInfoHolder">
        <div @click="jumpToRCP">
          <div class="CSSName"> {{this.CSStaffBaseInfo.staffName}}</div>
          <div class="CSSId">{{this.CSStaffBaseInfo.CSSId}}</div>
        </div>
        <a-button icon="slack" @click="this.showUpload" type="dashed"  :style="{ fontSize: '12px',color:'#382C77'}" style="margin-left: 40px">
          更新声纹
        </a-button>
      </div>
    </div>
<!--todo 圆形客服头像 下面每个字体的美化，增加一些icon和颜色-->
    <div class="CSSFootContainer">
      <div>{{"沟通案例"}} </div>
      <div>{{this.CSStaffBaseInfo.NumOfCase}}</div>
      <div>{{"服务评价"}}</div>
      <div>{{this.CSStaffBaseInfo.serviceEvaluation.toFixed(2)}}</div>
    </div>

    <a-modal
      title="更新客服声纹"
      :visible="this.visible"
      @ok="handleOk"
      @cancel="handleCancel"
    >
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
import { mapGetters, mapActions, mapMutations } from 'vuex'
import {change_staff_voice_print_api} from "@/api/CSStaff";

export default {
  name: "CSSCard",

  props: {
    CSStaffBaseInfo:{},
    // recordId:"",
  },
  data() {
    return {
      customerServiceAvatar: require("../assets/service.png"),
      visible:false,
      fileList: [],
    };
  },
  mounted() {
  },
  methods: {
    ...mapMutations([
      'set_curCaseCSS',
      'set_curSelectedRecordEmpty'
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
        formData.append('CSSId',this.CSStaffBaseInfo.CSSId)
        formData.append('file',this.fileList[0])
        let res = await change_staff_voice_print_api(formData)
        console.log(res)
        if(res){
          let status = res.code
          if (status === 200) {
            this.$message.success(`${this.CSStaffBaseInfo.CSSId}客服 声纹更新成功`);
          } else {
            this.$message.error(`${this.CSStaffBaseInfo.CSSId}客服 声纹上传失败 ${res.message}`);
          }
        }
      }
      this.fileList = []
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
    jumpToRCP(){
      let _this=this;
      let data=this.CSStaffBaseInfo;
      this.set_curCaseCSS(data);
      this.set_curSelectedRecordEmpty();
      console.log("点击 jumpToRCP");
      this.$router.push("/recordCasePage")
    },
  }
}
</script>

<style scoped>
.CSSCard-container{
  padding-left: 10px;
  padding-top: 10px;
  width: 340px;
  height: 100px;
  background-color: rgba(236,235,248, 0.8);
  border-radius: 3px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}
.Info-container{
  width: 100%;
  height: 60px;
  display: flex;
  align-items: center
}
.imgHolder{
  margin-right: 20px;
  border-radius: 25px;
  width: 50px;
  height: 50px;
}
.CSSInfoHolder{
  width: 300px;
  height: 50px;
  display: flex;
  align-items: center
}
.CSSFootContainer{
  display: flex;
  align-items: center;
}
</style>
