<template>
  <div>
    <el-menu
      class="el-menu-vertical-demo"
      router
      background-color="white"
      :default-openeds="['1','2']"
      :default-active="nowpath"
    >
      <el-menu-item style="color: grey;font-size: xx-small" @click="logout">退出{{username}}</el-menu-item>
      <el-menu-item index="/home">回到首页</el-menu-item>
      <el-submenu index="1">
        <template slot="title">
          <i class="el-icon-menu"></i>
          <span>功能区</span>
        </template>
        <el-menu-item index="/project">项目管理</el-menu-item>
        <el-menu-item index="/task">任务面板</el-menu-item>
        <el-menu-item index="/env">环境管理</el-menu-item>
      </el-submenu>

      <el-submenu index="2">
        <template slot="title">
          <i class="el-icon-menu"></i>
          <span>维护区</span>
        </template>
        <a href="http://localhost:8000/admin"><el-menu-item>进入后台</el-menu-item></a>
        <a href="http://localhost:8000/admin/auth/user"><el-menu-item>用户管理</el-menu-item></a>

        <el-menu-item>任务面板</el-menu-item>
        <el-menu-item>环境管理</el-menu-item>
      </el-submenu>

    </el-menu>

  </div>
</template>

<script>
export default {
  name: "Menu",
  data(){
    return{
      username:'',
      nowpath:window.location.href.split('#')[1].split('?')[0]
    }
  },
  methods:{
    logout(){
        sessionStorage.clear()
        window.location.href = '/'
    },
  },
  mounted() {
    this.username=sessionStorage.getItem('username')
    // 防止直接通过http://localhost:8080/#/home访问，强行跳转到登录页面
    if(this.username==null){
      window.location.href = '/'
    }
  }
}
</script>

<style scoped>
 a{
   text-decoration: none;
   color: black;
 }
 span{
   box-shadow: 4px 4px 8px grey;
   padding:5px 20px ;
 }
</style>