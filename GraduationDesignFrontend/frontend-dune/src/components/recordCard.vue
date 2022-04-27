<template>
  <div class="recordCard-container" @click="jumpToRCA">
    <div class="recordInfo">
      <a-icon type="bar-chart" :style="{ fontSize: '24px',color:'#418AB3'}" />
      <div class="typicalPoint">{{this.recordBaseInfo.typicalPoint}}</div>
    </div>
    <div :id='this.recordBaseInfo.key' class="audioPicEchars">
    </div>
    <div class="footContainer">
      <div class="CSSInfo">
        <div class="CSSNameContainer" style="display: flex;align-items: center">
          <a-icon type="customer-service" :style="{ fontSize: '18px',color:'#1A5599'}"/>
          <div class="CSSName">{{this.recordBaseInfo.staffName}}</div>
        </div>

        <div class="CostumerIdContainer" style="display: flex;align-items: center">
          <a-icon type="CSStaff" :style="{ fontSize: '18px',color:'#1A5599'}"/>
          <div class="CostumerId">{{"   "+this.recordBaseInfo.staffId}}</div>
        </div>

      </div>
      <div  class="emotionTagContainer">
        <a-tag v-for="(tagInfo,i) in this.emotionTag" :key="i" :color="tagInfo.color" >
          {{tagInfo.name}}
        </a-tag>
      </div>
    </div>


  </div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from 'vuex'
export default {
  name: "recordCard",
  props: {
    recordBaseInfo:{},

  },
  data() {
    return {
      data: [],
      emotionTag:[],
    };
  },

  async mounted() {
    console.log("传入card")
    console.log(this.recordBaseInfo);

    let emotionList=this.recordBaseInfo.emotions;
    let emotionTag=[];
    for (let i = 0; i < emotionList.length; i++) {
      let data={};
      let emotion=emotionList[i];
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
      emotionTag.push(data);
    }
    this.emotionTag=emotionTag

    await this.getLoudnessData(this.recordBaseInfo.caseName,this.recordBaseInfo.staffId)
    this.echartsInit();
  },
  methods: {
    ...mapMutations([
      'set_curSelectedRecord'
    ]),
    ...mapActions([
      'getLoudness',
    ]),

    jumpToRCA(){
      let _this=this;
      let data=this.recordBaseInfo;

      this.set_curSelectedRecord(data);
      console.log("点击 jumpToRCA");
      this.$router.push("/recordCaseAnalysis")
      // this.$router.push("/recordCaseAnalysis/"+_this.recordId)
    },

    async getLoudnessData(caseName,staffId){
      let params = {
        caseName: caseName,
        staffId: staffId
      }
      let loudness = await this.getLoudness(params)
      this.data=loudness
    },

    echartsInit: function () {
      let chartDom = document.getElementById(this.recordBaseInfo.key+'');
      let myChart = this.$echarts.init(chartDom);
      let option;
    // 数据处理
      let timeList=this.data.map(function (item) {
        return item[0];
      });
      let valueList=this.data.map(function (item) {
        return item[1];
      });
      option = {
        // Make gradient line here
        gradientColor:["#fbf292","#f09125","#db5e3c", "#e80404",],
        visualMap: [
          {
            show: false,
            type: 'continuous',
            seriesIndex: 0,
            min: 0,
            max: 1500,
            handleStyle:{
              indicatorSize:'85%'
            }
          }
        ],

        grid:[{
          left:"1%",
          right:"1%",
          top:10,
          bottom:10
        }],

        tooltip: {
          trigger: 'axis'
        },
        xAxis: [
          {
            data: timeList,
            show: false//隐藏x轴
          },
        ],
        yAxis: [
          {splitLine:{show: false},//去除网格线
            show: false//隐藏y轴
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
    }
  }
}
</script>

<style scoped>
.recordCard-container{
  padding-left: 10px;
  padding-top: 10px;
  width: 330px;
  height: 170px;
  background-color:rgba(234,241,250,0.7);
  border-radius: 6px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
}
.recordInfo{
  width: 100%;
  display: flex;
}
.recordName{
  margin-left: 10px;
}

.recordId{
  margin-left: 10px;

}
.CSSName{
  margin-left: 10px;
  color: #9499A0;
}
.CostumerId{
  margin-left: 10px;
  color: #9499A0;
}
.audioPicEchars{
  width: 100%;
  height: 80px;
}
.footContainer{
  width: 100%;
  height:50px;
  display: flex;
  justify-content:space-between;

}
.CSSInfo{
  width: 35%;
  height: 100%;
}
.emotionTagContainer{
  width: 50%;
  height: 100%;
}
</style>
