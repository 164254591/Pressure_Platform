<template>
  <div class="login">
    <el-card style="float: right;width: 400px;height: 280px;margin-right: 35%">
      <h2>欢迎登录压测平台</h2>
      <el-form :model="form_data" >
        <el-form-item>
          <el-input prefix-icon="el-icon-user-solid" clearable v-model="form_data.username" placeholder="请输入用户名">{{form_data.username}}</el-input>
        </el-form-item>

        <el-form-item>
          <el-input prefix-icon="el-icon-lock" clearable v-model="form_data.password" placeholder="请输入密码" show-password>{{form_data.password}}</el-input>
        </el-form-item>
      </el-form>
      <el-button type="success" @click="login">登录</el-button>
      <el-button type="primary" @click="register">注册</el-button>


    </el-card>

    <el-carousel :interval="2000" type="card" height="200px">
      <el-carousel-item v-for="i in 3" :key="i" style="border-radius: 15px;box-shadow: 4px 4px 8px black">
      <img :src="require('../assets/'+i+'.png')" style="height: 100%;width: 100%">
      </el-carousel-item>
    </el-carousel>

  </div>

</template>

<script>
import axios from 'axios'
export default {
  name: "Login",
  data(){
    return{
       form_data:{
         username:'',
         password:'',
        }
    }
  },
  methods:{
    login(){
      axios.post('/login_account/',this.form_data).then(res=>{
        if(res.data.code===0){
          this.$message({
            message:'登录成功！',
            type:'success',
            duration:700,
          })
          // 用户名写入session
          sessionStorage.setItem('username',this.form_data.username)
          //跳转到首页
          this.$router.replace('/home')
        }else{
          this.$message({
            message:'用户名或密码错误！',
            type:'error'
          })
        }
      })
    },
    register(){
      axios.post('register_account/',this.form_data).then(res=>{
        if(res.data.code===0){
          this.$message({
            message:'恭喜你，注册成功！',
            type:'success'
          })
        }
        else {
          this.$message({
            message:'用户名已存在，注册失败！',
            type:'error'
          })
        }
      })
    },

  },
  mounted() {

  },
}
</script>

<style scoped>
.login {
  width: 100%;
  height: 100%;
  padding-top: 150px;
  background-image: url("../assets/login.jpeg");
  background-size: 100% 100%;
  background-position: center center;
  overflow: auto;
  position: fixed;
}
</style>