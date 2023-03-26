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
                  :on-success="get_script_list"
              >
                <el-button size="mini" type="primary">上传脚本</el-button>
                <span style="font-size: xx-small;color: darkgray">（上传同名脚本会覆盖）</span>
              </el-upload>
            </el-form-item>
            <el-form-item label="压测计划:" style="text-align: left;">
              <el-input v-model="project_detail.plan"></el-input>
            </el-form-item>
            <el-form-item label="计划说明:" style="text-align: left">
              <span style="font-size: xx-small;text-align: left;">
                (多个阶段用英文逗号,隔开，每秒发一轮;请不要忽略压测机性能而随意填充大数字进行压测)<br>
                【常量压测】0-5-2:下标为0(指第一个脚本)的脚本执行2轮，每轮次5个并发 <br>
                【阶梯压测】0-10/90-5：下标为0的脚本执行5轮，并发量从10逐步增加到90，即10,30,50,70,90 <br>

              </span>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="run_visible=true">加入队列</el-button>
              <el-button @click="restore">恢复默认</el-button>
            </el-form-item>

          </el-form>
        </el-main>
      </el-container>
    </el-container>

    <el-dialog :close-on-click-modal='false' title="新建任务队列..." :visible.sync="run_visible">
      <el-input v-model="des" placeholder="请输入任务描述"></el-input>
      <br><br>
      <el-button @click="run">确定</el-button>
      <el-button @click="run_visible=false">取消</el-button>

    </el-dialog>

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
      des:'',
      run_visible:false,

    }
  },
  methods: {
    restore(){
      window.location.reload()
    },
    run(){
      axios.post('/save_project/',this.project_detail).then(res=>{
        axios.get('/add_tasks/',{
          params:{
            des:this.des,
            project_id:this.project_detail.id
          }
        }).then(res=>{
          this.run_visible=false;
          this.$message({
          message:'保存成功！',
          type:"success",
        })
        })
      });
    },
    get_action(){
      return process.env.VUE_APP_BASE_URL+'/upload_script_file/'
    },
    get_script_list(){
       axios.get('/get_script_list/').then(res=>{
      this.script_list=res.data
        });
    }

  },
  mounted() {
    axios.get('/get_project_detail/',{
      params:{
        project_id:this.$route.query.project_id
      }}).then(res=>{
        this.project_detail=res.data
    });

    this.get_script_list();

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