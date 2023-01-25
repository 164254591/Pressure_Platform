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
      <el-button type="success">登录</el-button>
      <el-button type="primary">注册</el-button>


    </el-card>

    <el-carousel :interval="1000" type="card" height="200px">
      <el-carousel-item v-for="i in 3" :key="i" style="border-radius: 15px;box-shadow: 4px 4px 8px black">
      <img :src="require('../assets/'+i+'.png')" style="height: 100%;width: 100%">
      </el-carousel-item>
    </el-carousel>

  </div>

</template>

<script>
export default {
  name: "Login",
  data(){
    return{
       form_data:{
         username:'',
         password:'',
        }
    }
  }
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