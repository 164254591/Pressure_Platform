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
        <el-menu-item @click="project_list_visible=true">项目管理</el-menu-item>
        <el-menu-item @click="get_tasks" >任务面板</el-menu-item>
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

    <el-dialog  title="项目列表" :visible.sync="project_list_visible" style="line-height:18px;width: 100%;">
      <el-table :data="projects">
        <el-table-column prop="id" label="编号" width="50px"></el-table-column>
        <el-table-column prop="name" label="名称"></el-table-column>
        <el-table-column prop="plan" label="计划" ></el-table-column>
        <el-table-column width="150px">
          <template slot="header">
            <el-button style="width: 121px" @click="add_project">新增项目</el-button>
          </template>
          <template slot-scope="scope">
            <router-link :to="'/project_detail/?project_id='+scope.row.id">
              <el-button size="mini" type="success" @click="into(scope.row.id)">进入</el-button>
            </router-link>
            &nbsp;
            <el-button size="mini" type="danger" @click="delete_project(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>

      </el-table>
    </el-dialog>
    <el-dialog :before-close="close_tasks" title="任务面板" width="60%" :visible.sync="task_visible" style="line-height:18px;width:80%">
      <el-table :data="tasks">
        <el-table-column prop="id" label="编号" width="50px"></el-table-column>
        <el-table-column prop="project_id" label="项目id"></el-table-column>
        <el-table-column prop="stime" label="创建时间" width="180px"></el-table-column>
        <el-table-column  label="状态" >
          <template slot-scope="scope">
            <p :style="{color:getColor(scope.row.status)}"><strong>{{ scope.row.status }}</strong></p>
          </template>
        </el-table-column>
        <el-table-column prop="des" label="任务描述" ></el-table-column>
        <el-table-column label='操作' width="150px">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="into(scope.row.id)">报告</el-button>
            <el-button size="mini" type="danger" @click="delete_project(scope.row.id)">终止</el-button>
          </template>
        </el-table-column>

      </el-table>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: "Menu",
  data(){
    return{
      projects:[],
      project_list_visible:false,
      username:'',
      nowpath:window.location.href.split('#')[1].split('?')[0],
      task_visible:false,
      tasks:[],
    }
  },
  methods:{
    getColor(status){
      if(status=='队列中'){
        return 'blue'
      }else if (status=='压测中'){
        return 'green'
      }else{
        return 'black'
      }
    },
    logout(){
        sessionStorage.clear()
        window.location.href = '/'
    },
    add_project(){
      axios.get('/add_project/').then(res=>{
        this.projects=res.data
      })
    },
    delete_project(project_id){
      axios.get('/delete_project/',{
        params:{
        project_id:project_id
        }}).then(res=>{
        this.projects=res.data
      })
    },
    into(id){
      this.$router.push('/project_detail/?project_id='+id);
      this.$router
      window.location.reload()
    },
    get_tasks(){
      this.task_visible=true;
      this.get_tasks_act();
      //自动重复执行
      this.t1 = setInterval(()=>{
        this.get_tasks_act()
      },1000)
    },
    close_tasks(done){
      clearInterval(this.t1)
      done()
    },
    get_tasks_act(){
      axios.get('/get_tasks/').then(res=>{
        this.tasks=res.data
      })
    }

  },
  mounted() {
    this.username=sessionStorage.getItem('username')
    // 防止直接通过http://localhost:8080/#/home访问，强行跳转到登录页面
    if(this.username==null){
      window.location.href = '/'
    };
    axios.get('/get_projects/').then(res=>{
      this.projects=res.data
    })


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