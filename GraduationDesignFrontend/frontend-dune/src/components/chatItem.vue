<!--聊天框中的message组件-->
<template>
  <div class="record-wrapper">
    <div class="time">{{ displayedTime }}</div>

    <div v-if="from == 1" class="msg msg-right">
      <div class="img-wrapper">
        <a-avatar class="img">{{this.userName}}</a-avatar>
        <a-tag :color="this.tagInfo.color" style="margin-top: 10px" >
          {{this.tagInfo.name}}
        </a-tag>
      </div>
      <div class="message-wrapper message-wrapper-right">
        <div class="message">{{ message }}</div>
      </div>
    </div>

    <div v-if="from == 2" class="msg msg-left">
      <div class="img-wrapper">
        <img class="img" :src="from2"/>
        <a-tag :color="this.tagInfo.color" style="margin-top: 10px" >
          {{this.tagInfo.name}}
        </a-tag>
      </div>
      <div class="message-wrapper message-wrapper-left">
        <div class="message" v-html="message"></div>
      </div>
    </div>

    <div v-if="from == 3" class="msg_recommend">
<!--      <div class="img-wrapper">-->
<!--        <img class="img" :src="from2"/>-->
<!--        <a-tag :color="this.tagInfo.color" style="margin-top: 10px" >-->
<!--          {{this.tagInfo.name}}-->
<!--        </a-tag>-->
<!--      </div>-->
      <div class="recommend_message-wrapper message-wrapper-mid">
        <div class="recommend_message" v-html="message"></div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "chatItem",
    props: {
      from: Number, // 1: 自己    2: 别人
      message: String,
      timestamp: Date,
      displayedTime: String,
      userName: String,
      tagInfo:{},
    },
    data() {
      return {
        from2: require("../assets/service.png"),
      };
    },
    mounted() {
      // console.log(this.message)
    }
  };
</script>

<style lang="scss" scoped>
  .record-wrapper {
    user-select: text;
    margin: 4px;
    padding: 4px;
  }

  .time {
    text-align: center;
    font-size: smaller;
    margin: .5em;
  }

  .msg {
    display: flex;
    flex-direction: row;

    .message-wrapper {
      max-width: 240px;
      margin: 0px 10px 0px 10px;
      .message {
        margin: 6px 8px 2px 8px;
        font-size: small;
        word-wrap: break-word; //英文换行
      }
    }


    .message-wrapper-left {
      margin-top: 5px;
      border-radius: 0px 5px 5px 5px;
      background-color: rgb(236,235,248);
    }

    .message-wrapper-right {
      margin-top: 5px;

      background-color: rgb(234,241,250);
      border-radius: 5px 0px 5px 5px;
    }
    .img-wrapper{
     height: 60px;
      width: 42px;
    }
    .img {
      flex: auto;
      height: 36px;
      width: 36px;
      border-radius: 18px;
      padding-top: 2px;
      margin-left: 5px;
      margin-right: 5px;
      /*border: solid white 2px;*/
    }
  }

  .msg-right {
    flex-direction: row-reverse;
  }

  .msg-left {
    flex-direction: row;
  }

  .msg_recommend {

    .recommend_message-wrapper{
      width: 380px;
      margin:10px auto;
      border-radius: 5px 5px 5px 5px;
      background-color: rgb(246,246,246);
      .recommend_message {
        width: 320px;
        margin:0 auto;
        padding-top: 20px;
        padding-bottom: 20px;
        font-size: small;
        word-wrap: break-word; //英文换行
        white-space: pre-line;
      }
    }
  }
</style>
