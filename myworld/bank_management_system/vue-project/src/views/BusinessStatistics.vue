<template>
    <el-row justify="space-around">
      <el-space warp>
        <el-card class="box-card" style="width: 800px">
          <el-container>
            <el-header height="50px">
              <el-radio-group v-model="radio" @change="radioChange">
                <el-radio-button label="Monthly"/>
                <el-radio-button label="Seasonly"/>
                <el-radio-button label="Yearly"/>
              </el-radio-group>
            </el-header>
    
            <el-main>
              <el-scrollbar height="200px">
                <el-table :data="statistics">
                  <el-table-column prop="branch_name" label="Branch Name"/>
                  <el-table-column prop="account_num" label="Account Number"/>
                  <el-table-column prop="saving" label="Saving"/>
                  <el-table-column prop="loan" label="Lending"/>
                </el-table>
              </el-scrollbar>
            </el-main>
          </el-container>
        </el-card>
      </el-space>
  
    </el-row>
  </template>
  
  
<script>
  import axios from "axios";
  
  const apiUrl = 'http://localhost:8000/api/'
  
  export default {
    name: "BusinessStatistics",
    data() {
      return {
        radio: 'Monthly',
        statistics: [
          {
            'branch_name': '',
            'account_num': 0,
            'saving': 0,
            'loan': 0,
          },
        ],
      }
    },
    mounted() {
      this.radioChange('Monthly')
    },
    methods: {
      radioChange: function (radio) {
        axios.post(apiUrl + 'branch/statisticize/', {'radio': radio})
          .then(response => {
            this.statistics = response.data
          })
      },
    }
  }
</script>
  