<template>
<div class="caseAnalysisContainer">
  <div class="subBreadcrumb">
    <div class="RecordTitle">
      <a  @click="goBackHome" class="title" style="height: 25px">我的工作台</a>
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
            案例分析
          </a-breadcrumb-item>
        </a-breadcrumb>
      </div>
    </div>
    <div class="CSSInfo">
      <div class="CSSName"></div>
      <div class="CSSPortrait"></div>
    </div>

  </div>
  <div class="panelCells">

    <div class="panelLeft">

      <div class="subTitle1" style=" font-size: 1.45rem;font-weight: 600;margin-top: 20px;margin-left: 20px">#音频对话</div>

      <div class="chatMessagesWrapper">
        <chat-item
          v-for="item in chatMessages"
          :key="item.key"
          :type="item.type"
          :message="item.message"
          :timestamp="item.timestamp"
          :displayedTime="item.displayedTime"
          :from="item.from"
          :userName="name"
          :tagInfo="item.tagInfo"
        ></chat-item>
        <a-spin :spinning="spinning">
        </a-spin>
        <a-button size="large" @click="doRecommend()" block>
          为当前案例进行智能推荐
        </a-button>
      </div>

    </div>
    <div class="panelRight">
      <div id='LoudnessDiagram' class="LoudnessDiagramEchars">
      </div>
      <div id='EmotionalChangeDiagram' class="EmotionalChangeEchars">
      </div>
      <div style="display: flex;align-content: center;justify-content: flex-start;">
        <div class="subTitle2" style="font-size: 1.45rem;font-weight: 600;width:25px;padding:0;margin-right: 30px;margin-top: 40px;line-height: 25px">#案例评价</div>
        <div class="case_evaluation_wrapper">
          <div id='caseScoringRadar' class="radarEchars"> </div>
          <div class="evaluation_details">
            {{"客服自身情绪不良 "+this.caseEvaluationData.staffPessimisticNum+"次，情绪良好 "+this.caseEvaluationData.staffOptimisticNum+"次\n"+
          "客户自身情绪不良 "+this.caseEvaluationData.customerPessimisticNum+"次，情绪良好 "+this.caseEvaluationData.customerPessimisticNum+"次\n"+
          "客服使用礼貌用语的比例为 "+this.caseEvaluationData.staffPoliteWordsPercent+"%\n"+
          this.caseEvaluationData.customerSatisfied + "\n"+
          this.caseEvaluationData.staffUnderstandProblem + "\n"+
          this.caseEvaluationData.staffSolveProblem + "\n"
            }}
          </div>

        </div>
      </div>

    </div>
<!--    <div class="panelRight">-->
<!--      <div class="subTitle3" style="font-size: 18px;margin-top: 20px;margin-left: 20px">客服评价</div>-->
<!--    </div>-->

  </div>

</div>
</template>

<script>
const ChatItem = ()=>import("./chatItem.vue");
import {mapActions, mapGetters, mapMutations} from 'vuex'

export default {
name: "recordCaseAnalysis",
  components: {
    "chat-item": ChatItem
  },
  computed: {
    ...mapGetters([
      'chatMessages',
      'curSelectedRecord',
      'curCaseCSS',
    ])
  },
  async mounted() {
    // 发送请求，请求具体的data！！
    await this.getCurCaseCSS(this.curSelectedRecord.staffId)
    await this.getCaseAnalysisData();

    this.name = "客户";
    let box = document.getElementsByClassName('chatMessagesWrapper')[0];
    box.scrollTop = box.scrollHeight;
    this.lastTime = this.chatMessages[this.chatMessages.length - 1].timestamp;

    console.log("进入到 案例分析页");
    console.log(this.curSelectedRecord);

    this.LoudnessEchartsInit();
    this.EmotionalChangeEchartsInit()
    this.radarEchartsInit();

  },
  data() {
    return {
      name: "",
      spinning: false,
      lastTime: {},
      content: '',
      loudnessData:[],
      emotionTimeData:[['0:00',500]
        ,['0:10',400],['0:20',300]
        ,['0:30',200],['0:40',150],['0:50',400],['0:60',300],],
      curRecommendIndex:0,
      case_dialogue_list:[],
      recommendation_point_list:[],
      caseEvaluationData:{},
      case_score_list:[0,0,0,0,0,0]
    };
  },
  methods: {
    ...mapMutations([
      'set_curCaseCSS',
      'set_message'
    ]),
    ...mapActions([
      'getLoudness',
      'getCaseDialogueList',
      'getRecommendationPointList',
      'getCaseEvaluation',
      'getCurCaseCSS'
    ]),
    async getCaseAnalysisData(){
      await this.getCaseDialogueListData(this.curSelectedRecord.caseName,this.curSelectedRecord.staffId)
      await this.getRecommendationPointListData(this.curSelectedRecord.caseName,this.curSelectedRecord.staffId)
      await this.getLoudnessData(this.curSelectedRecord.caseName,this.curSelectedRecord.staffId)
      await this.getCaseEvaluationData(this.curSelectedRecord.caseName,this.curSelectedRecord.staffId)
      // 拿到 当前案例的分析数据；
      // let CurCaseAnalysisData= await this.getCurCaseAnalysisData();
      //处理拿到的 聊天记录，成为数据展示；
      await this.conversation_handler();
    },

    async getCaseDialogueListData(caseName,staffId){
      let params = {
        caseName: caseName,
        staffId: staffId
      }
      let dialogue = await this.getCaseDialogueList(params)
      this.case_dialogue_list = dialogue
      this.setEmotionTimeData()
    },

    setEmotionTimeData(){
      // {min: 600, max: 700,label: '感谢'},
      // {min: 500, max: 600,label: '开心'}, // 不指定 max，表示 max 为无限大（Infinity）。
      // {min: 400, max: 500,label: '平静'},
      // {min: 300, max: 400,label: '抱怨'},
      // {min: 200, max: 300,label: '悲伤'},
      // {min: 100, max: 200,label: '愤怒'},
      // {min: 0, max: 100,label: '情绪'},
      // if(emotion=="angry"){
      //   data={color:"red", name:"愤怒"}
      //
      // }else if(emotion=="happy"){
      //   data={color:"yellow", name:"开心"}
      // }else if(emotion=="neutral"){
      //   data= {color:"green", name:"平静"}
      // }else if(emotion=="thankful"){
      //   data= {color:"purple", name:"感谢"}
      // }else if(emotion=="complaining"){
      //   data= {color:"pink", name:"抱怨"}
      // }else if(emotion=="sad"){
      //   data={color:"blue", name:"悲伤"}
      // }
      let emotion_num_map = {
        thankful: 600,
        happy: 500,
        neutral: 400,
        complaining: 300,
        sad: 200,
        angry: 100
      }
      let customer_dialogues = this.case_dialogue_list.filter(item=>item.role==="customer")
      this.emotionTimeData = []
      for(let i = 0;i<customer_dialogues.length;i++)
        this.emotionTimeData.push([i,emotion_num_map[customer_dialogues[i].emotion]])
      // console.log(customer_dialogues)
    },

    async getRecommendationPointListData(caseName,staffId){
      let params = {
        caseName: caseName,
        staffId: staffId
      }
      let recommendation = await this.getRecommendationPointList(params)
      this.recommendation_point_list = recommendation
    },

    async getLoudnessData(caseName,staffId){
      let params = {
        caseName: caseName,
        staffId: staffId
      }
      let loudness = await this.getLoudness(params)
      this.loudnessData=loudness
    },

    async getCaseEvaluationData(caseName,staffId){
      let params = {
        caseName: caseName,
        staffId: staffId
      }
      let evaluation = await this.getCaseEvaluation(params)
      this.caseEvaluationData=evaluation
      this.caseEvaluationData.staffPoliteWordsPercent=this.caseEvaluationData.staffPoliteWordsPercent.toFixed(2);
      // {name: '客服情绪', max: 100, color: 'rgba(0, 0, 0, 0.55)'},
      // {name: '客户情绪', max: 100, color: 'rgba(0, 0, 0, 0.55)'},
      // {name: '客户满意', max: 100, color: 'rgba(0, 0, 0, 0.55)'},
      // {name: '解决问题', max: 100, color: 'rgba(0, 0, 0, 0.55)'},
      // {name: '理解问题', max: 100, color: 'rgba(0, 0, 0, 0.55)'},
      // {name: '礼貌用语', max: 100, color: 'rgba(0, 0, 0, 0.55)'},
      this.case_score_list = [
        evaluation.staffEmotionScore,
        evaluation.customerEmotionScore,
        evaluation.customerSatisfiedScore,
        evaluation.staffSolveProblemScore,
        evaluation.staffUnderstandProblemScore,
        evaluation.staffPoliteWordsPercent
      ]
      console.log("拿到getCaseEvaluation")
      console.log(evaluation)
    },

    async conversation_handler () {
        let chatMessageList=[];
        let _this=this;
        for(let i=0;i<_this.case_dialogue_list.length;i++){
          let item=_this.case_dialogue_list[i];
          let emotionTag=await _this.gen_tag(item.emotion);
          if(item.role=="service"){
            chatMessageList.push({
                type: 1,
                message: item.message,
                key: chatMessageList.length,
                from: 2,
                timestamp: new Date(),
                displayedTime: '',
                userName: "客服",
                tagInfo:emotionTag,
              })
          }else {
            chatMessageList.push({
              type: 1,
              message: item.message,
              key: chatMessageList.length,
              from: 1,
              timestamp: new Date(),
              displayedTime: '',
              userName: "USER",
              tagInfo:emotionTag,
            })
          }
        }
        // console.log("完成对话处理");
        // console.log(chatMessageList);
        this.set_message(chatMessageList);

    },
    async gen_tag (emotion){
      let data={};
      if(emotion=="angry"){
        data={color:"red", name:"愤怒"}

      }else if(emotion=="happy"){
        data={color:"yellow", name:"开心"}
      }else if(emotion=="neutral"){
        data= {color:"green", name:"平静"}
      }else if(emotion=="thankful"){
        data= {color:"purple", name:"感谢"}
      }else if(emotion=="complaining"){
        data= {color:"pink", name:"抱怨"}
      }else if(emotion=="sad"){
        data={color:"blue", name:"悲伤"}
      }
      return data
    },

    doRecommend: function () {
      // 一次三条，进行尝试；
      let recommendation_point_list_size=this.recommendation_point_list.length;
      // 截断逻辑
      if(this.curRecommendIndex==recommendation_point_list_size){

        console.log("进入截断逻辑")
        this.chatMessages.push({
          type: 1,
          message: "本案例无更多推荐点",
          key: this.chatMessages.length,
          from: 3,
          timestamp: new Date(),
          displayedTime: '',
          name: "系统推荐"
        });

        return
      }

      if(recommendation_point_list_size-this.curRecommendIndex<3){// 准备结束 3-0=3
        // console.log(recommendation_point_list_size);
        // console.log(this.curRecommendIndex);
        // console.log("推荐结尾阶段")
        let curIndex=this.curRecommendIndex;
        let curRecommendEnd=recommendation_point_list_size;
        let _this=this;
        for(;curIndex<curRecommendEnd;curIndex++){
          this.chatMessages.push({
            type: 1,
            message: _this.recommendation_point_list[curIndex],
            key: this.chatMessages.length,
            from: 3,
            timestamp: new Date(),
            displayedTime: curIndex==0?'--------------------以下为案例推荐--------------------':"",
            name: "系统推荐"
          });
        }
        this.curRecommendIndex=curIndex;

        this.chatMessages.push({
          type: 1,
          message: "本案例无更多推荐点",
          key: this.chatMessages.length,
          from: 3,
          timestamp: new Date(),
          displayedTime: '--------------------已无更多推荐--------------------',
          name: "系统推荐"
        });


      }else { //当前 下标到结尾，大于3
        // console.log(recommendation_point_list_size);
        // console.log(this.curRecommendIndex);
        // console.log("推荐中间阶段")

        let curIndex=this.curRecommendIndex;
        let curRecommendEnd=Math.min(curIndex+3, recommendation_point_list_size);
        let _this=this;
        for(;curIndex<curRecommendEnd;curIndex++){
          this.chatMessages.push({
            type: 1,
            message: _this.recommendation_point_list[curIndex],
            key: this.chatMessages.length,
            from: 3,
            timestamp: new Date(),
            displayedTime: curIndex==0?'--------------------以下为案例推荐--------------------':"",
            name: "系统推荐"
          });
        }
        this.curRecommendIndex=curIndex;

      }


    },
    // displayedTime: '--------------------以下为案例推荐--------------------',
    goBackHome(){
      this.$router.push("/homepage")
    },
    LoudnessEchartsInit: function () {
      let chartDom = document.getElementById('LoudnessDiagram');
      let myChart = this.$echarts.init(chartDom);
      console.log('chartDom')
      console.log(chartDom)
      let option;
      // 数据处理
      let dateList=this.loudnessData.map(function (item) {
        return item[0];
      });
      let valueList=this.loudnessData.map(function (item) {
        return item[1];
      });
      option = {
        // Make gradient line here
        title: {
          text: '音频响度图'
        },
        gradientColor:["#fbf292","#f09125","#db5e3c", "#e80404",],
        visualMap: [
          {
            show: true,
            type: 'continuous',
            seriesIndex: 0,
            min: 70,
            max: 300,
            handleStyle:{
              indicatorSize:'95%'
            }
          }
        ],

        grid:[{
          left:"8%",
          right:"5%",
          bottom:"15%",
          containLabel: true
        }],

        tooltip: {
          trigger: 'axis'
        },
        xAxis: [
          {
            data: dateList,
            show: true//隐藏x轴
          },
        ],
        yAxis: [
          {splitLine:{show: true},//去除网格线
            show: true//隐藏y轴
          },
        ],
        series: [
          {
            type: 'line',
            showSymbol: false,
            data: valueList
          },
        ]
      };
      myChart.setOption(option);
    },
    EmotionalChangeEchartsInit: function () {
      let chartDom = document.getElementById('EmotionalChangeDiagram');
      let myChart = this.$echarts.init(chartDom);
      let option;
      // 数据处理
      let timeList=this.emotionTimeData.map(function (item) {
        return item[0];
      });
      let valueList=this.emotionTimeData.map(function (item) {
        return item[1];
      });
      option={
        gradientColor:["#fbf292","#f09125","#db5e3c", "#e80404","#e70404"],
        visualMap: [
          {
            show: false,
            type: 'piecewise',
            seriesIndex: 0,
            min: 100,
            max: 500,
            handleStyle:{
              indicatorSize:'95%'
            },
            pieces: [
              {min: 600, max: 700,label: '感谢'}, // 不指定 max，表示 max 为无限大（Infinity）。
              {min: 500, max: 600,label: '开心'},
              {min: 400, max: 500,label: '平静'},
              {min: 300, max: 400,label: '抱怨'},
              {min: 200, max: 300,label: '悲伤'},
              {min: 100, max: 200,label: '愤怒'},
              {min: 0, max: 100,label: '情绪'},
            ]
          }
        ],
        title: {
          text: '客户情绪变化图'
        },
        tooltip: {
          trigger: 'axis'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '5%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data:timeList
          // data: dateList
        },
        yAxis: {
          type: 'value',
          axisLabel:{
            //函数模板
            formatter:function (value, index) {
              var result="";
              // {min: 600, max: 700,label: '感谢'}, // 不指定 max，表示 max 为无限大（Infinity）。
              // {min: 500, max: 600,label: '开心'},
              // {min: 400, max: 500,label: '平静'},
              // {min: 300, max: 400,label: '抱怨'},
              // {min: 200, max: 300,label: '悲伤'},
              // {min: 100, max: 200,label: '愤怒'},
              // {min: 0, max: 100,label: '情绪'},
              switch(value){
                case 0:result="未知情绪";break;
                case 100:result="愤怒";break;
                case 200:result="悲伤";break;
                case 300:result="抱怨";break;
                case 400:result="平静";break;
                case 500:result="开心";break;
                case 600:result="感谢";break;
                default:"-";
              }
              return result;
            }
          }
        },
        series: [
          {
            // name: 'Step Start',
            type: 'line',
            step: 'start',
            data:valueList
            // data: valueList
          },
        ]
      };
      //情绪数值映射
      // ['开心', '平静', '愤怒', '悲伤', '未知情绪']
      // ['500', '400', '300', '200', '100']


      /*option = {*/
      /*  // Make gradient line here*/
      /*  gradientColor:["#fbf292","#f09125","#db5e3c", "#e80404",],*/
      /*  visualMap: [*/
      /*    {*/
      /*      show: true,*/
      /*      type: 'continuous',*/
      /*      seriesIndex: 0,*/
      /*      min: 70,*/
      /*      max: 300,*/
      /*      handleStyle:{*/
      /*        indicatorSize:'95%'*/
      /*      }*/
      /*    }*/
      /*  ],*/

      /*  grid:[{*/
      /*    left:"8%",*/
      /*    right:"5%",*/
      /*    top:"5%",*/
      //     bottom:"15%"
      //   }],
      //
      //   tooltip: {
      //     trigger: 'axis'
      //   },
      //   xAxis: [
      //     {
      //       data: dateList,
      //       show: true//隐藏x轴
      //     },
      //   ],
      //   yAxis: [
      //     {splitLine:{show: true},//去除网格线
      //       show: true//隐藏y轴
      //     },
      //   ],
      //   series: [
      //     {
      //       type: 'line',
      //       showSymbol: false,
      //       data: valueList
      //     },
      //   ]
      // };

      myChart.setOption(option);
    },
    radarEchartsInit: function () {
      // console.log("开始渲染echarts")
      // console.log(this.showed);
      let roseCharts = document.getElementById("caseScoringRadar");
      let myChart = this.$echarts.init(roseCharts);


      myChart.setOption({
        backgroundColor: 'white',
        radar: {
          // shape: 'circle',
          nameGap: 5,
          center: ['50%', '50%'],
          radius: '65%',
          indicator: [
            {name: '客服情绪', max: 100, color: 'rgba(0, 0, 0, 0.55)'},
            {name: '客户情绪', max: 100, color: 'rgba(0, 0, 0, 0.55)'},
            {name: '客户满意', max: 100, color: 'rgba(0, 0, 0, 0.55)'},
            {name: '解决问题', max: 100, color: 'rgba(0, 0, 0, 0.55)'},
            {name: '理解问题', max: 100, color: 'rgba(0, 0, 0, 0.55)'},
            {name: '礼貌用语', max: 100, color: 'rgba(0, 0, 0, 0.55)'},
          ],
        },
        grid: {
          position: 'center',
        },
        series: [{
          type: 'radar',
          data: [
            {
              value: this.case_score_list,
              name: '各项评分',
              itemStyle: {
                normal: {
                  color: 'rgb(230, 32, 33)',

                },
              },
            },
          ]
        }],
      })
    },

  }
}
</script>

<style lang="scss" scoped>
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
.panelCells{
  margin-top: 3px;
  padding-top: 30px;
  display: flex;
  height: 93vh;
  width: 100%;
  padding-left: 12vw;
  background-color: #F9F9F9;
}
.panelLeft{
  height: 86vh;
  width: 30vw;
  background-color: #FFFFFF;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
.chatMessagesWrapper{
  padding: 5px;
  overflow: auto;
  height: 80vh;
}

/*.panelMid{*/
/*  height: 86vh;*/
/*  width: 40vw;*/
/*  margin-left: 20px;*/
/*  background-color: #FFFFFF;*/
/*  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);*/
/*}*/
.panelRight{
  height: 86vh;
  width: 55vw;
  padding: 35px 35px 20px 40px;
  margin-left: 20px;
  background-color: #FFFFFF;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  .case_evaluation_wrapper{
    width: 660px;
    display: flex;
    align-content: center;
    justify-content: space-between;
    .radarEchars {
      height: 250px;
      width: 270px;
      background-color: white;
    }
    .evaluation_details{
      width: 350px;
      height: 250px;
      line-height: 1.85;
      font-family: Tahoma,Helvetica,Arial,'宋体',sans-serif;
      color: #51596A;
      font-size: 1.1em;
      font-weight: 600;
      white-space: pre-line;
    }
  }
}


.LoudnessDiagramEchars{
  width: 40vw;
  height: 200px;
}
.EmotionalChangeEchars{
  width: 40vw;
  height: 200px;
}
</style>
