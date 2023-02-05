<template>
  <div style="height: 100%">
    <el-container style="height: 100%">
      <el-aside width="200px">
        <Menu></Menu>
      </el-aside>

      <el-container>
        <el-header>
          <h1>欢迎查看项目{{ $route.query.project_id }}的详情页 </h1>
        </el-header>

        <el-main>
          <el-form :model="project_detail" label-width="80px">
            <el-form-item label="项目ID:" style="text-align: left">
              {{project_detail.id}}
            </el-form-item>
            <el-form-item label="项目名称:" style="text-align: left;">
              <el-input v-model="project_detail.name"></el-input>
            </el-form-item>
            <el-form-item label="脚本列表:" style="text-align: left;">
              <el-select v-model="project_detail.scripts" multiple placeholder="请选择脚本" style="width: 100%">
                <el-option
                  v-for="(i,index) in script_list"
                  :label="'【'+index+'】'+i"
                  :value="i"
                >
                </el-option>
              </el-select>

              <el-upload
                  style="float: left"
                  :action="get_action()"
                  :limit="1"
                  name="script_file"
              >
                <el-button size="mini" type="primary">上传脚本</el-button>
                <span style="font-size: xx-small;color: darkgray">（上传同名脚本会覆盖）</span>
              </el-upload>
            </el-form-item>
            <el-form-item label="压测计划:" style="text-align: left;">
              <el-input v-model="project_detail.plan"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="save_project">保存</el-button>
              <el-button @click="restore">恢复默认</el-button>
            </el-form-item>

          </el-form>
        </el-main>
      </el-container>
    </el-container>

  </div>
</template>

<script>

import Menu from "@/components/Menu";
import axios from "axios";


export default {
  name: "ProjectDetail",
  data() {
    return {
      project_detail:{},
      script_list:[],

    }
  },
  methods: {
    restore(){
      window.location.reload()
    },
    save_project(){
      axios.post('/save_project/',this.project_detail).then(res=>{
        this.$message({
          message:'保存成功！',
          type:"success",
        })
      })
    },
    get_action(){
      return process.env.VUE_APP_BASE_URL+'/upload_script_file/'
    }

  },
  mounted() {
    axios.get('/get_project_detail/',{
      params:{
        project_id:this.$route.query.project_id
      }}).then(res=>{
        this.project_detail=res.data
    });
    axios.get('/get_script_list/').then(res=>{
      this.script_list=res.data
        });


  },
  components: {
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

p {
  font-size: small;

}
</style>