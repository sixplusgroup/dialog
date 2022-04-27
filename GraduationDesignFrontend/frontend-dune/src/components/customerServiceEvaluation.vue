<template>
  <div class="serviceEvalContainer">
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
              客服评价
            </a-breadcrumb-item>
          </a-breadcrumb>
        </div>
      </div>
      <div class="CSSInfo">
        <div class="CSSName"></div>
        <div class="CSSPortrait"></div>
      </div>

    </div>
=    <div class="panelCells">
      <div class="panelCenter">
        <div class="subTitle2" style="font-size: 1.45rem;font-weight: 600;margin-bottom: 15px">#客服评价</div>
<!--        this.staffEvaluation.score.toFixed(2)-->
        <div class="service_evaluation"> {{"目前"+this.curCaseCSS.staffName+"的评分为： "+this.staffEvaluation.score+"分"}}</div>
        <div id='StaffHistoryScoreDiagram' class="LoudnessDiagramEchars">
        </div>

        <div class="case_evaluation_wrapper">
          <div class="evaluation_detail_left">
            {{"相比上次"+diff+diffScore+"分\n"+
          "近期的成长趋势为"+this.staffEvaluation.shortTermGrowthTrend+"\n"+
          "长期的成长趋势为"+this.staffEvaluation.longTermGrowthTrend+"\n\n"+
          "累计有效服务"+this.staffEvaluation.serviceNum+"次\n"+
          "明显未能解决问题的比例为"+this.staffEvaluation.problemUnsolvedPercent+"%\n"+
          "问题处理能力"+this.staffEvaluation.problemSolve+"\n"+
          "平均通话时长为"+this.staffEvaluation.averageTime+"秒\n"+
          "时长"+this.staffEvaluation.averageTimeDescription+"\n\n"+
          "有效案例平均得分为"+this.staffEvaluation.averageCaseScore+"分\n"
            }}
          </div>
          <div class="evaluation_detail_right">
            {{"客服累计出现不良情绪"+this.staffEvaluation.staffPessimisticNum+"次\n"+
          "客服出现不良情绪的通话比例为"+this.staffEvaluation.staffPessimisticPercent+"%\n"+
          "客服自身的情绪控制能力"+this.staffEvaluation.staffEmotionControlAbility+"\n\n"+
          "客户累计出现不良情绪"+this.staffEvaluation.customerPessimisticNum+"次\n"+
          "客户出现不良情绪的通话比例为"+this.staffEvaluation.customerPessimisticPercent+"%\n"+
          "引导客户情绪的能力"+this.staffEvaluation.customerEmotionControlAbility+"\n\n"+
          "礼貌用语的使用"+this.staffEvaluation.politeWordsUsage+"\n"+
          "平均语速为"+this.staffEvaluation.averageSpeechSpeed+"词/分钟，"+this.staffEvaluation.speechSpeed+"\n"+
          "昔通话发音平均得分为"+this.staffEvaluation.averagePronunciationScore+"分\n"
            }}
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations} from 'vuex'
export default {
  name: "customerServiceEvaluation",
  computed:{
    ...mapGetters([
      'curCaseCSS',
    ]),
  },
  async mounted() {
    // 发送请求，请求具体的data！！
    let staffHistoryScores = await this.getStaffHistoryScores()
    console.log(staffHistoryScores)
    this.data = staffHistoryScores
    let previous_score = 0
    let latest_score = 0
    if(staffHistoryScores.length>0)
      latest_score = staffHistoryScores[staffHistoryScores.length-1][1]
    if(staffHistoryScores.length>1)
      previous_score = staffHistoryScores[staffHistoryScores.length-2][1]
    let diff_score = latest_score-previous_score
    if(diff_score>=0){
      this.diff = '进步'
      this.diffScore = diff_score.toFixed(2)
    }
    else{
      this.diff = '退步'
      this.diffScore = (-1*diff_score).toFixed(2)
    }
    let tempStaffEvaluation= await this.getStaffEvaluation()
    console.log("tempStaffEvaluation");
    console.log(tempStaffEvaluation);
    tempStaffEvaluation.problemUnsolvedPercent=tempStaffEvaluation.problemUnsolvedPercent.toFixed(2);
    tempStaffEvaluation.averageTime=tempStaffEvaluation.averageTime.toFixed(2);
    tempStaffEvaluation.averageCaseScore=tempStaffEvaluation.averageCaseScore.toFixed(2);
    tempStaffEvaluation.staffPessimisticPercent=tempStaffEvaluation.staffPessimisticPercent.toFixed(2);
    tempStaffEvaluation.customerPessimisticPercent=tempStaffEvaluation.customerPessimisticPercent.toFixed(2);
    tempStaffEvaluation.averageSpeechSpeed=tempStaffEvaluation.averageSpeechSpeed.toFixed(2);
    tempStaffEvaluation.averagePronunciationScore=tempStaffEvaluation.averagePronunciationScore.toFixed(2);


    tempStaffEvaluation.score=tempStaffEvaluation.score.toFixed(2);

    this.staffEvaluation=tempStaffEvaluation
    console.log(tempStaffEvaluation);

    this.HistoryScoreEchartsInit();
  },
  data() {
    return {
      staffName:'',
      staffEvaluation:{},
      diff:'',
      diffScore:0,
      data:[["2000-06-05", 116], ["2000-06-06", 129], ["2000-06-07", 135], ["2000-06-08", 86], ["2000-06-09", 73], ["2000-06-10", 85], ["2000-06-11", 73], ["2000-06-12", 68], ["2000-06-13", 92], ["2000-06-14", 130], ["2000-06-15", 245], ["2000-06-16", 139], ["2000-06-17", 115], ["2000-06-18", 111], ["2000-06-19", 309], ["2000-06-20", 206], ["2000-06-21", 137], ["2000-06-22", 128], ["2000-06-23", 85], ["2000-06-24", 94], ["2000-06-25", 71], ["2000-06-26", 106], ["2000-06-27", 84], ["2000-06-28", 93], ["2000-06-29", 85], ["2000-06-30", 73], ["2000-07-01", 83], ["2000-07-02", 125], ["2000-07-03", 107], ["2000-07-04", 82], ["2000-07-05", 44], ["2000-07-06", 72], ["2000-07-07", 106], ["2000-07-02", 125], ["2000-07-03", 107], ["2000-07-04", 82], ["2000-07-05", 44], ["2000-07-06", 72], ["2000-07-07", 106]],
    };
  },
  methods: {
    ...mapActions([
      'getStaffEvaluation',
      'getStaffHistoryScores'
    ]),
    goBackHome: function(){
      this.$router.push("/homepage")
    },
    HistoryScoreEchartsInit: function () {
      console.log('HistoryScoreEchartsInit')
      console.log(this.data)
      console.log(this.staffEvaluation)
      let chartDom = document.getElementById('StaffHistoryScoreDiagram');
      console.log('chartDom')
      console.log(chartDom)
      let myChart = this.$echarts.init(chartDom);
      let option;
      // 数据处理
      let dateList=this.data.map(function (item) {
        return item[0];
      });
      let valueList=this.data.map(function (item) {
        return item[1];
      });
      option = {
        // Make gradient line here
        title: {
          text: '分数变化图'
        },
        gradientColor:["#fbf292","#f09125","#db5e3c", "#e80404",],
        visualMap: [
          {
            show: true,
            type: 'continuous',
            seriesIndex: 0,
            min: 0,
            max: 100,
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
   align-content: center;

   height: 93vh;
   width: 100%;
   padding-left: 12vw;
   background-color: #F9F9F9;


  .panelCenter{
    margin-left: 8vw;
    height: 86vh;
    width: 53vw;
    padding: 30px 40px 20px 40px;
    background-color: #FFFFFF;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    .service_evaluation{
      margin-bottom: 15px;
      font-family: Tahoma,Helvetica,Arial,'宋体',sans-serif;
      color: #51596A;
      font-size: 1.2em;
      font-weight: 600;
      white-space: pre-line;
    }
    .LoudnessDiagramEchars{
      width: 40vw;
      height: 200px;
    }

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
      .evaluation_detail_left{
        width: 350px;
        height: 240px;
        line-height: 1.85;
        font-family: Tahoma,Helvetica,Arial,'宋体',sans-serif;
        color: #51596A;
        font-size: 1.1em;
        font-weight: 600;
        white-space: pre-line;
      }
      .evaluation_detail_right{
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
}



</style>
