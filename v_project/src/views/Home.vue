<template>
  <div style="height: 100%">
    <el-container style="height: 100%">
      <el-aside width="200px">
        <Menu></Menu>
      </el-aside>

      <el-container>
        <el-header>
          <h1>欢迎来到首页,{{ username }}</h1>
        </el-header>

        <el-main>
          <el-card style="height:-webkit-calc(100% - 410px);width:30%;float:left">
            <div slot="header" class="clearfix">
              项目概览
            </div>
            <p>平台项目数</p>
            <p>平台项目数</p>
            <p>平台项目数</p>

          </el-card>
          <el-card style="height:-webkit-calc(100% - 410px);width:-webkit-calc(70% - 5px)">
            <div slot="header" class="clearfix">
              正在运行的压测任务
            </div>
          </el-card>
          <el-card style="height: 400px">
            <div slot="header" class="clearfix">
              历史压测结果
            </div>
          </el-card>
        </el-main>
      </el-container>
    </el-container>

  </div>
</template>

<script>

import Menu from "@/components/Menu";

export default {
  name: "Home",
  data() {
    return {
      username: '',
    }
  },
  methods: {
    logout() {
      // 清空前端session
      sessionStorage.clear()
      // 退出到首页
      window.location.href = '/'
    }
  },
  mounted() {
    this.username = sessionStorage.getItem('username')
  },
  components:{
    Menu,
}
}
</script>

<style scoped>
.el-header {
  background-color: #B3C0D1;
  color: #333;
  text-align: center;
  line-height: 60px;
  border-bottom: 1px solid #c1c1c1;
}

.el-aside {
  background-color: #D3DCE6;
  color: #333;
  border-right: grey;
  text-align: center;
  line-height: 200px;
}

.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
  /*line-height: 160px;*/
}

.el-card {
  background-color: white;
  text-align: left;
  overflow-y: auto;
}
p{
  font-size: small;

}
</style>