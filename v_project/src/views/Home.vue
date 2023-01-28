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
            <p>平台项目数：20</p>
            <p>历史项目数：53</p>
            <p>平台用户数：92</p>

          </el-card>
          <el-card style="height:-webkit-calc(100% - 410px);width:-webkit-calc(70% - 5px)">
            <div slot="header" class="clearfix">
              正在运行的压测任务
            </div>
            <span style="font-size: xx-small">任务1</span>
            <el-progress :percentage="50"></el-progress>
            <span>任务2</span>
            <el-progress :percentage="100" :format="format"></el-progress>
            <span>任务3</span>
            <el-progress :percentage="100" status="success"></el-progress>
            <span>任务4</span>
            <el-progress :percentage="100" status="warning"></el-progress>
            <span>任务5</span>
            <el-progress :percentage="50" status="exception"></el-progress>
          </el-card>
          <el-card style="height: 400px">
            <div slot="header" class="clearfix">
              历史压测结果
            </div>
            <div id="myChart" style="width:100%;height: 300px"></div>
          </el-card>
        </el-main>
      </el-container>
    </el-container>

  </div>
</template>

<script>

import Menu from "@/components/Menu";
import axios from "axios";

//导入echarts
let echarts = require('echarts/lib/echarts')
require('echarts/lib/chart/line')
require('echarts/lib/component/tooltip')
require('echarts/lib/component/title')
require('echarts/lib/component/legend')
import {GridComponent} from 'echarts/components'

echarts.use([GridComponent]);


export default {
  name: "Home",
  data() {
    return {
      username: '',
      option: {
        legend: {data: []}, //标题
        xAxis: {
          type: 'category',
          data: [],
          name: '日期',
          nameTextStyle: {
            fontWeight: 400, //字体宽度
            fontSize: 15,
            color: 'green',
          },
          axisTick: {
            show: true, //显示刻度
            alignWithLabel: true, //对齐文案
            interval: '0',//刻度间距
            length: 5,//标尺长度
            inside: false,
          },
          axisLabel: {
            interval: '0',
            rotate: 0, //角度旋转
          },
        },
        yAxis: {
          type: 'value',
          name: '压测次数',
          nameTextStyle: {
            fontWeight: 400,
            fontSize: 15,
          }
        },
        label: {},
        tooltip: {trigger: 'item'},
        series: [],
      }
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
    this.username = sessionStorage.getItem('username');

    axios.get('/get_echarts_data/').then(res => {
      this.option.legend.data = res.data.legend_data;
      this.option.xAxis.data = res.data.xAxis_data;
      this.option.series = res.data.series;
      let myChart = echarts.init(document.getElementById('myChart'),'dark')
      myChart.setOption(this.option)
    })
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