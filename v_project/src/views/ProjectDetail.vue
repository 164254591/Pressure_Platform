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
            <el-form-item label="压测计划:">
              <el-table :data="project_detail.plan">
                <el-table-column label="脚本名" >
                  <template  slot-scope="scope">
                    <el-select v-model="scope.row.name" placeholder="请选择">
                      <el-option
                        v-for="i in script_list"
                        :label="i"
                        :value="i"
                      >
                      </el-option>
                    </el-select>
                  </template>

                </el-table-column>
                <el-table-column label="原始并发数">
                  <template slot-scope="scope">
                    <el-input v-model="scope.row.old_num"></el-input>
                  </template>
                </el-table-column>
                 <el-table-column label="原始轮数">
                  <template slot-scope="scope">
                    <el-input v-model="scope.row.old_round"></el-input>
                  </template>
                </el-table-column>
                <el-table-column>
                  <template slot="header">
                    <el-button size="mini" type="primary" @click="add_step">新增阶段</el-button>
                  </template>
                  <template slot-scope="scope">
                    <el-button size="mini" type="danger" @click="del_step(scope.$index)">删除阶段</el-button>
                  </template>
                </el-table-column>

              </el-table>

            </el-form-item>

            <el-form-item label="计划说明:" style="text-align: left">
              <span style="font-size: xx-small;text-align: left;">
                (每阶段运行完后才会运行下一轮，每秒发一轮;请不要忽略压测机性能而随意填充大数字进行压测)<br>
                【常量压测】0-5-2:下标为0(指第一个脚本)的脚本执行2轮，每轮次5个并发 <br>
                【阶梯压测】0-10/90-5：下标为0的脚本执行5轮，并发量从10逐步增加到90，即10,30,50,70,90 <br>
                【无限增压】0-10+5：下标为0的脚本从10并发，每轮增加5并发（安全阈值为100轮）,注意增量不要太大 <br>
                【瞬时增压】0-10_100_1000-5:下标为0的脚本从10并发执行5轮后，突然增压到100并发并执行5轮后，再突然增压到1000并发并执行5轮

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
    add_step(){
      this.project_detail.plan.push({'name': '', 'old_num': '', 'old_round': ''})
    },
    del_step(index){
      this.project_detail.plan.splice(index,1)
    },
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