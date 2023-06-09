<template>
    <el-container>
      <el-main>
        <el-space wrap>
          <el-card class="box-card" style="width: 550px">
            <el-table :data="loanData" table-layout="auto" max-height="590" height="590">
              <el-table-column fixed prop="id" label="Id" />
              <el-table-column prop="total" label="Total" />
              <el-table-column prop="balance" label="Balance" />
              <el-table-column prop="release_date" label="Release Date" />
              <el-table-column prop="branch_name" label="Branch Name" width="125"/>
              <el-table-column prop="staff_id" label="Staff ID" >
              </el-table-column>
            </el-table>
          </el-card>
          
          <el-card class="box-card" style="width: 400px">
            <el-table :data="clientLoanData" table-layout="auto" max-height="590" height="590" @row-click="fillInput">
              <el-table-column prop="client_id" label="Client Id"/>
              <el-table-column prop="loan_id" label="Loan Id"/>
              <el-table-column prop="status" label="Status" />
            </el-table>
          </el-card>
        </el-space>
      </el-main>
      
      <el-aside width="300px">
        <div style="min-height: 20px;"></div>
        <el-card class="box-card">
          <el-form>
            <el-form-item v-for="field in clientLoanFields" :key="field.name" :label="field.label">
              <el-input v-model="field.searchRef"/>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="searchLoan">Search</el-button>
            </el-form-item>
          </el-form>
        </el-card>
  
        <el-card class="box-card">
          <el-form>
            <el-form-item v-for="field in inputFields" :key="field.name" :label="field.label">
              <el-input v-model="field.inputRef"/>
            </el-form-item>
            <el-form-item>
              <el-dialog
                v-model="openDialog"
                title="Confirm"
                width="30%"
              >
                <span>
                  <el-descriptions :column="1" border>
                    <el-descriptions-item v-for="i in addList" :label="inputFields[i].label"
                                          :key="inputFields[i].name" width="110px">
                      {{ inputFields[i].inputRef }}
                    </el-descriptions-item>
                  </el-descriptions>
                </span>
                <template #footer>
                  <span class="dialog-footer">
                    <el-button @click="openDialog = false">Cancel</el-button>
                    <el-button type="primary" @click="releaseLoan">Confirm</el-button>
                  </span>
                </template>
              </el-dialog>
              <el-button type="primary" @click="openDialog = true">Release</el-button>
              <el-button type="warning" @click="updateLoan">Update</el-button>
              <el-popconfirm
                :title="'Are you sure you want to delete ' + inputFields[3].inputRef + '?'"
                cancel-button-type="primary"
                cancel-button-text="No"
                confirm-button-type="danger"
                confirm-button-text="Yes"
                @confirm="deleteLoan"
              >
                <template #reference>
                  <el-button type="danger">Delete</el-button>
                </template>
              </el-popconfirm>
            </el-form-item>
          </el-form>
        </el-card>
      </el-aside>
    </el-container>
  </template>
    
    
  <script>
    import axios from "axios";
    import {ElMessage} from "element-plus";
    
    const clientLoanFields = [
      {'name': 'client_id', 'label': 'ID'},
      {'name': 'loan_id', 'label': 'Loan ID'},
      {'name': 'status', 'label': 'Status'}
    ]
    clientLoanFields.forEach(field => field['searchRef'] = '')
    
    const inputFields = [
      {'name': 'client_id', 'label': 'ID'},
      {'name': 'client_name', 'label': 'Name'},
      {'name': 'loan_id', 'label': 'Loan ID'},
      {'name': 'total', 'label': 'Total'},
      {'name': 'balance', 'label': 'Balance'},
      {'name': 'release_date', 'label': 'Release Date'},
      {'name': 'branch_name', 'label': 'Branch Name'},
      {'name': 'staff_id', 'label': 'Staff ID'},
    ]
    inputFields.forEach(field => field['inputRef'] = '')
  
    const addList = [0, 3, 6, 7]
    const updateList = [2, 4]
    
    const apiUrl = 'http://localhost:8000/api/'
    const loanUrl = 'http://localhost:8000/api/loan/'
  
    export default {
      data() {
        return {
          clientLoanFields,
          inputFields,
          addList,
          queryUrl: apiUrl + 'client_loan/?',
          openDialog: false,
          loanData:[],
          clientLoanData: [],
        }
      },
      created() {
        this.fetchItems();
      },
      mounted() {
        this.searchLoan()
      },
      methods: {
        fetchItems() {
          axios.get(loanUrl)
            .then(response => {
              this.loanData = response.data;
            })
            .catch(error => {
              console.error(error);
            });
        },
  
        searchLoan: async function () {
          this.queryUrl = apiUrl + 'client_loan/?'
          clientLoanFields.forEach(field => {
            if(field.searchRef)
                this.queryUrl += field.name + '=' + field.searchRef + '&'
          })
          this.clientLoanData = (await axios.get(this.queryUrl)).data
        },
    
        fillInput: function (client_loan) {
          this.inputFields[0].inputRef = client_loan['client_id']
          axios.get(apiUrl + 'client/' + client_loan['client_id'] + '/')
            .then(response => this.inputFields[1].inputRef = response.data['name'])
    
          if(client_loan['loan_id']) {
            this.inputFields[2].inputRef = client_loan['loan_id']
            axios.get(apiUrl + 'loan/' + client_loan['loan_id'] + '/')
              .then(response => {
                this.inputFields[3].inputRef = response.data['total']
                this.inputFields[4].inputRef = response.data['balance']
                this.inputFields[5].inputRef = response.data['release_date']
                this.inputFields[6].inputRef = response.data['branch_name']
                this.inputFields[7].inputRef = response.data['staff_id']
              })
          }
          else for(let i = 3; i <= 7; i++) this.inputFields[i].inputRef = ''
        },
    
        releaseLoan: function () {
          this.openDialog = false
          let data = {}
          addList.forEach(i => data[inputFields[i].name] = inputFields[i].inputRef)
          axios.post(apiUrl + 'client_loan/release_loan/', data)
              .then(response => {
                if(response.status === 201) {
                  ElMessage({
                    message: 'Success',
                    type: 'success'
                  })
                }
              })
              .catch(error => {
                console.log(error)
                ElMessage({
                  message: 'Error: ' + error.response.data,
                  type: 'error'
                })
              })
        },
    
        updateLoan: function () {
          if(!inputFields[2].inputRef){
            ElMessage({
              message: 'No loan id',
              type: 'error'
            })
            return
          }
          let data = {}
          updateList.forEach(i => data[inputFields[i].name] = inputFields[i].inputRef)
          axios.put(apiUrl + 'loan/' + inputFields[2].inputRef + '/', data)
            .then(response => {
              if(response.status === 200){
                ElMessage({
                  message: 'Success',
                  type: 'success'
                })
              }
            })
            .catch(error => {
              console.log(error)
              ElMessage({
                  message: 'Error: ' + error.response.data,
                  type: 'error'
                })
            })
        },
    
        deleteLoan: function () {
          axios.delete(apiUrl + 'loan/' + inputFields[2].inputRef + '/')
            .then(resopnse => {
              if(resopnse.status === 204){
                ElMessage({
                  message: 'Success',
                  type: 'success'
                })
              }
            })
            .catch(error => {
              console.log(error)
              ElMessage({
                message: 'Error: ' + error.response.data,
                type: 'error'
              })
            })
        }
      }
    }
  </script>
    