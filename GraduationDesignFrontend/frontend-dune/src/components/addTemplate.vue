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
            <a-breadcrumb-item>
              添加模板
            </a-breadcrumb-item>
          </a-breadcrumb>
        </div>
      </div>
      <div class="CSSInfo">
        <div class="CSSName">{{this.curCaseCSS.staffName}}</div>
        <div class="CSSName">{{this.curCaseCSS.CSSId}}</div>
      </div>

    </div>
    <div class="recordPageContent">
      <div class="panelCells">
        <div style="height:25px; width: 100%; font-size: 1.2rem;font-weight: 600; margin-left: 8px">
          <a-icon type="form" style="font-size: small"/>
          <span>添加话术模板</span>
        </div>
        <a-divider style="height: 1px; background-color: #9499A0;margin-left: 9px;margin-right: 9px" />
        <div style="height: 80%; width: 100%; margin-top: 35px">
          <a-form
            name="basic"
            :label-col="{ span: 5 }"
            :wrapper-col="{ span: 16 }"
            @submit="submit"
          >
            <a-form-item label="类型">
              <a-radio-group v-model:value="formState.type" @change="change_type">
                <a-radio-button value="skill">首尾话术</a-radio-button>
                <a-radio-button value="template">客服模板</a-radio-button>
              </a-radio-group>
            </a-form-item>
            <a-form-item
              v-show="show_skill"
              label="话术主题"
              name="type"
              margin-bottom="60px"
            >
              <a-radio-group
                :rules="[{ required: true, message: '请选择一个主题！' }]"
                v-model:value=formState.theme
              >
                <a-radio value="1">开头话术</a-radio>
                <a-radio value="2">结尾话术</a-radio>
              </a-radio-group>
            </a-form-item>
            <a-form-item
              v-show="show_template"
              label="模板主题"
              name="type"
              margin-bottom="60px"
            >
              <a-radio-group
                :rules="[{ required: true, message: '请选择一个主题！' }]"
                v-model:value=formState.theme
              >
                <a-radio value="1">语句转换</a-radio>
                <a-radio value="2">站在客户利益角度发言</a-radio>
                <a-radio value="3">拒绝的艺术</a-radio>
              </a-radio-group>
            </a-form-item>

            <a-form-item
              label="模板内容"
              name="content"
            >
              <a-textarea
                v-model:value=formState.content
                :rules="[{ required: true, message: '请输入模板内容!' }]"
              ></a-textarea>
            </a-form-item>

            <a-form-item :wrapper-col="{ offset: 10, span: 16 }">
              <a-button type="primary" html-type="submit">提交</a-button>
            </a-form-item>
          </a-form>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
  import {add_template} from "@/api/CSStaff";
  import {mapActions, mapGetters} from "vuex";

  export default {
    name: "recordCasePage",
    data() {
      return {
        formState:{
          type:'',
          theme:'',
          content:''
        },
        show_skill:false,
        show_template:false
      }
    },
    computed: {
      ...mapGetters([
        'curCaseCSS'
      ]),
    },
    async mounted() {
      console.log("进入 添加话术模板 页");
    },
    methods: {
      change_type(){
        console.log(this.formState.type)
        if(this.formState.type==="skill"){
          this.show_template=false;
          this.show_skill=true;
        }else{
          this.show_skill=false;
          this.show_template=true;
        }
      },
      async submit(){
        console.log("信息：",this.formState)
        if(this.formState.type===""){
          this.$message.error(`请选择类型`);
        }else if(this.formState.theme===""){
          this.$message.error(`请选择主题`);
        }else if(this.formState.content===""){
          this.$message.error(`请填写模板内容`);
        }else{
          const formData = new FormData()
          formData.append('type',this.formState.type)
          formData.append('theme',this.formState.theme)
          formData.append('content',this.formState.content)
          let res = await add_template(formData)
          console.log(res)
          if(res) {
            let status = res.code;
            if (status === 200) {
              this.$message.success(`添加话术模板成功`);
              this.reset();
            } else {
              this.$message.error(`添加话术模板失败 ${res.message}`);
            }
          }
        }
      },
      reset(){
        this.formState.type=''
        this.formState.theme=''
        this.formState.content=''
      },
      goBackHome(){
        this.$router.push("/homepage")
      },
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
  .panelCells{
    margin-top: 2vw;
    padding-top: 40px;
    padding-left: 50px;
    padding-right: 50px;
    float: left;

    height: 80vh;
    width: 60%;
    margin-left: 5vw;
    background-color: #FFFFFF;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }



</style>
