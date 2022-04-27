<template>
  <div class="main">
    <div class="login-left">
      <h1 style="font-weight: bolder;font-size: 50px" >Autopia</h1>
      <a-form
        id="formLogin"
        class="user-layout-login"
        ref="formLogin"
        :form="form"
      >
        <a-tabs
          :activeKey="customActiveKey"
          :tabBarStyle="{ textAlign: 'center', borderBottom: 'unset' }"
          @change="handleTabClick"
        >
          <a-tab-pane key="tab1" tab="登录">
            <a-form-item class="formItem">
              <a-input class="login-input"
                       size="large"
                       type="text"
                       placeholder="用户名"
                       v-decorator="[
                'username',
                {rules: [{ required: true, message: '请输入用户名' }], validateTrigger: 'blur'}
              ]"
                       style="margin-bottom: .5em;margin-top: 2em"
              >
                <a-icon slot="prefix" type="CSStaff" :style="{ color: 'rgba(0,0,0,.25)' }"/>
              </a-input>
            </a-form-item>
            <a-form-item class="formItem">
              <a-input class="login-input"
                       size="large"
                       type="password"
                       autocomplete="false"
                       placeholder="密码"
                       v-decorator="[
                'password',
                {rules: [{ required: true, message: '请输入密码' }], validateTrigger: 'blur'}
              ]"
                       style="margin-bottom: .5em"
              >
                <a-icon slot="prefix" type="lock" :style="{ color: 'rgba(0,0,0,.25)' }"/>
              </a-input>
            </a-form-item>
            <a-form-item class="formItem" style="margin-top: 5em">
              <a-button
                size="large"
                type="primary"
                class="login-button"
                :loading="loginLoading"
                @click="handlelogin()"
              >确定
              </a-button>
            </a-form-item>
          </a-tab-pane>

          <a-tab-pane key="tab2" tab="注册">
            <a-form-item class="formItem">
              <a-input class="login-input"
                       size="large"
                       placeholder="用户名"
                       v-decorator="[
              'registerUsername',
              {rules: [{ required: true, message: '请输入用户名' }], validateTrigger: 'blur'}]"
                       style="margin-bottom: 3px">
                <a-icon slot="prefix" type="CSStaff" :style="{ color: 'rgba(0,0,0,.25)' }"/>
              </a-input>
            </a-form-item>
            <a-form-item class="formItem">
              <a-input class="login-input"
                       size="large"
                       type="password"
                       placeholder="密码"
                       v-decorator="[
                'registerPassword',
                {rules: [{ required: true, message: '请输入密码' }, { validator: this.handlePassword }], validateTrigger: 'blur'}]"
                       style="margin-bottom: 3px">
                <a-icon slot="prefix" type="lock" :style="{ color: 'rgba(0,0,0,.25)' }"/>
              </a-input>
            </a-form-item>
            <a-form-item class="formItem">
              <a-input class="login-input"
                       size="large"
                       type="password"
                       placeholder="确认密码"
                       v-decorator="[
                'registerPasswordconfirm',
                {rules: [{ required: true, message: '请输入密码' }, { validator: this.handlePasswordCheck }], validateTrigger: 'blur'}]"
                       style="margin-bottom: 3px">
                <a-icon slot="prefix" type="lock" :style="{ color: 'rgba(0,0,0,.25)' }"/>
              </a-input>
            </a-form-item>
            <a-form-item class="formItem">
              <a-button
                size="large"
                type="primary"
                class="login-button"
                :loading="registerLoading"
                @click="handleRegister()"
              >确定
              </a-button>
            </a-form-item>
          </a-tab-pane>
        </a-tabs>
      </a-form>
    </div>
    <div class="login-right">
<!--      <h1>Autopia</h1>-->
    </div>


  </div>
</template>

<script>
  import {mapGetters, mapActions,mapMutations} from 'vuex'

  export default {
    name: 'login',
    components: {},
    data() {
      return {
        customActiveKey: 'tab1',
        loginLoading: false,
        registerLoading: false,
        form: this.$form.createForm(this),
      }
    },
    computed: {
      ...mapGetters([
        'token',
        'chatMessages'
      ])
    },
    mounted() {

    },
    watch: {
      $route: {
        handler: function (route) {
          this.redirect = route.query && route.query.redirect
        },
        immediate: true
      },
    },
    methods: {
      ...mapActions([
        'login',
        'register'
      ]),
      ...mapMutations([
        'set_message',
      ]),

      handlePassword(rule, value, callback) {
        if (value.length < 6) {
          // callback(new Error('密码长度至少6位'))
        }
        callback()
      },
      handlePasswordCheck(rule, value, callback) {
        const password = this.form.getFieldValue('registerPassword')
        console.log(password);
        if (value === undefined) {
          callback(new Error('请输入密码'))
        }
        if (value && password && value.trim() !== password.trim()) {
          callback(new Error('两次密码不一致'))
        }
        callback()
      },
      handleTabClick(key) {
        this.customActiveKey = key
      },
      handlelogin() {
        this.set_message([
          {
            type: 1,
            key: 0,
            message: "能不能介绍一下奔驰E级？",
            from: 1,
            timestamp: new Date(),
            displayedTime: new Date().toLocaleDateString() + ' ' + new Date().toLocaleTimeString(),
            name:"USER"
          },
          {
            type: 1,
            key: 1,
            message: "以下是您所查找的车型介绍： " +"<br>"+
              "=======================" +"<br>"+
              "车型：奔驰E级" +"<br>"+
              "品牌：奔驰" +"<br>"+
              "类型：中大型车" +"<br>"+
              "指导价格：43.08-64.28万" +"<br>"+
              "驱动类型：" +"<br>"+
              "能源类型：汽油" +"<br>"+
              "变速箱类型：9挡手自一体" +"<br>"+
              "(电动车)充电时间：-" +"<br>"+
              "(电动车)续航时间：-" +"<br>"+
              "(油车)排量：1.5T 2.0T" +"<br>"+
              "综合评分：4.773087071240106''" ,
            from: 2,
            timestamp: new Date(),
            displayedTime: '',
            name:""
          },
        ])
        const validateFieldsKey = this.customActiveKey === 'tab1' ? ['username', 'password'] : ['registerUsername', 'registerPassword', 'registerPasswordconfirm']
        this.form.validateFields(validateFieldsKey, {force: true}, async (err, values) => {
          if (!err) {
            this.loginLoading = true;
            let formData = new FormData();
            formData.append("username", this.form.getFieldValue("username"));
            formData.append("password", this.form.getFieldValue("password"));

            await this.login(formData);
            this.loginLoading = false
          }
        })
      },

      handleRegister() {
        const {form: {validateFields}} = this
        const validateFieldsKey = this.customActiveKey === 'tab1' ? ['username', 'password'] : ['registerUsername', 'registerPassword', 'registerPasswordconfirm']
        validateFields(validateFieldsKey, {force: true}, async (err, values) => {
          if (!err) {
            this.registerLoading = true
            const data = {
              password: this.form.getFieldValue('registerPassword'),
              username: this.form.getFieldValue('registerUsername'),
            };

            await this.register(data).then(() => {
              // this.customActiveKey = 'tab1';
              this.form.setFieldsValue({
                'registerUsername': '',
                'registerPassword': '',
                'registerPasswordconfirm': ''
              })
            })
            this.registerLoading = false
          }
        });
      }
    }
  }
</script>

<style>
  #username {
    border-top-color: transparent;
    border-left-color: transparent;
    border-right-color: transparent;
    background-color: transparent;
  }

  #username:focus {
    box-shadow: 0 0 0;
    background-color: transparent;
  }

  #password {
    border-top-color: transparent;
    border-left-color: transparent;
    border-right-color: transparent;
    background-color: transparent;
  }

  #password:focus {
    box-shadow: 0 0 0;
    background-color: transparent;
  }

  #registerUsername {
    border-top-color: transparent;
    border-left-color: transparent;
    border-right-color: transparent;
    background-color: transparent;
  }

  #registerUsername:focus {
    box-shadow: 0 0 0;
    background-color: transparent;
  }

  #registerPassword {
    border-top-color: transparent;
    border-left-color: transparent;
    border-right-color: transparent;
    background-color: transparent;
  }

  #registerPassword:focus {
    box-shadow: 0 0 0;
    background-color: transparent;
  }

  #registerPasswordconfirm {
    border-top-color: transparent;
    border-left-color: transparent;
    border-right-color: transparent;
    background-color: transparent;
  }

  #registerPasswordconfirm:focus {
    box-shadow: 0 0 0;
    background-color: transparent;
  }

</style>


<style lang="less" scoped>

  .main {

    min-width: 260px;
    width: 100vw;
    height: 100vh;
    /*background: #000000 url('https://files.porsche.cn/filestore/image/multimedia/none/banner-ww-pds/normal/976296d6-15b6-11ea-80c6-005056bbdc38;s4/porsche-normal.jpg') no-repeat center;*/
    text-align: center;
    /*padding-top: 5em;*/
    background-image: url('../assets/zyb3.jpg');
    background-repeat: no-repeat;
    overflow: hidden;
    position: fixed;
    background-position: 0px 0px;
    background-size: 100% 100%;


    /*.top {*/
    /*  text-align: center;*/
    /*  padding-top: 100px;*/

    /*  .header {*/
    /*    height: 44px;*/
    /*    line-height: 44px;*/

    /*    .badge {*/
    /*      position: absolute;*/
    /*      display: inline-block;*/
    /*      line-height: 1;*/
    /*      vertical-align: middle;*/
    /*      margin-left: -12px;*/
    /*      margin-top: -10px;*/
    /*      opacity: 0.8;*/
    /*    }*/

    /*    .logo {*/
    /*      height: 44px;*/
    /*      vertical-align: top;*/
    /*      margin-right: 16px;*/
    /*      border-style: none;*/
    /*    }*/

    /*    .title {*/
    /*      font-size: 33px;*/
    /*      color: rgba(0, 0, 0, .85);*/
    /*      font-family: Avenir, 'Helvetica Neue', Arial, Helvetica, sans-serif;*/
    /*      font-weight: 600;*/
    /*      position: relative;*/
    /*      top: 2px;*/
    /*    }*/
    /*  }*/

    /*  .desc {*/
    /*    font-size: 14px;*/
    /*    color: rgba(0, 0, 0, 0.45);*/
    /*    margin-top: 12px;*/
    /*    margin-bottom: 40px;*/
    /*  }*/
    /*}*/
  }

  .formItem {
    margin-top: 3em;
    margin-bottom: 3em;
  }
  .login-left{
    background: rgba(255, 255, 255, 0.91);
    padding: 40px 50px;

    width: 400px;
    height: 100vh;

  }

  .user-layout-login {

    label {
      font-size: 14px;
    }

    .getCaptcha {
      display: block;
      width: 100%;
      /*height: 40px;*/
      height: 100%;
    }

    .forge-password {
      font-size: 14px;
    }

    button.login-button {
      padding: 0 15px;
      font-size: 16px;
      width: 100%;
    }

    .user-login-other {
      text-align: left;
      margin-top: 24px;
      line-height: 22px;

      .item-icon {
        font-size: 24px;
        color: rgba(0, 0, 0, 0.2);
        margin-left: 16px;
        vertical-align: middle;
        cursor: pointer;
        transition: color 0.3s;

        &:hover {
          color: #1890ff;
        }
      }

      .register {
        float: right;
      }
    }
  }
</style>
