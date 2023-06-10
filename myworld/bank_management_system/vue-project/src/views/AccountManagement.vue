<template>
  <el-container>
    <el-main>
      <el-space wrap>
        <el-card class="box-card" style="width: 550px">
          <el-table :data="accountData" style="width: 100%" max-height="740" height="740">
            <el-table-column fixed prop="id" label="Id" width="125" />
            <el-table-column prop="balance" label="Balance" width="175" />
            <el-table-column prop="register_date" label="Register Date" width="225" />
            <el-table-column prop="interest_rate" label="Interest Rate" width="150" />
            <el-table-column prop="currency_type" label="Currency Type" width="150" />
            <el-table-column prop="staff_id" label="Staff ID" width="125">
            </el-table-column>
          </el-table>
        </el-card>
        
        <el-card class="box-card" style="width: 400px">
          <el-table :data="clientBranchData" style="width: 100%" max-height="740" height="740" @row-click="fillInput">
            <el-table-column prop="client_id" label="Client Id"/>
            <el-table-column prop="branch_name" label="Branch Name"/>
            <el-table-column prop="account_id" label="Account Id"/>
          </el-table>
        </el-card>
      </el-space>
    </el-main>
    
    <el-aside width="285px">
      <div style="min-height: 20px;"></div>
      <el-card class="box-card">
        <el-form>
          <el-form-item v-for="field in clientBranchFields" :key="field.name" :label="field.label">
            <el-input v-model="field.searchRef"/>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="searchClientBranch">Search</el-button>
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
                  <el-button type="primary" @click="openAccount">Confirm</el-button>
                </span>
              </template>
            </el-dialog>
            <el-button type="primary" @click="openDialog = true">Open</el-button>
            <el-button type="warning" @click="updateAccount">Update</el-button>
            <el-popconfirm
              :title="'Are you sure you want to delete ' + inputFields[3].inputRef + '?'"
              cancel-button-type="primary"
              cancel-button-text="No"
              confirm-button-type="danger"
              confirm-button-text="Yes"
              @confirm="deleteAccount"
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
  
  const clientBranchFields = [
    {'name': 'client_id', 'label': 'ID'},
    {'name': 'branch_name', 'label': 'Branch Name'},
    {'name': 'account_id', 'label': 'Account ID'},
  ]
  clientBranchFields.forEach(field => field['searchRef'] = '')
  
  const inputFields = [
    {'name': 'client_id', 'label': 'ID'},
    {'name': 'client_name', 'label': 'Name'},
    {'name': 'branch_name', 'label': 'Branch Name'},
    {'name': 'account_id', 'label': 'Account ID'},
    {'name': 'currency_type', 'label': 'Currency Type'},
    {'name': 'balance', 'label': 'Balance'},
    {'name': 'interest_rate', 'label': 'Interest Rate'},
    {'name': 'staff_id', 'label': 'Staff ID'},
    {'name': 'register_date', 'label': 'Register Date'},
  ]
  inputFields.forEach(field => field['inputRef'] = '')

  const addList = [0, 2, 4, 6, 7]
  const updateList = [3, 4, 5, 6, 7, 8]
  
  const apiUrl = 'http://localhost:8000/api/'
  const accountUrl = 'http://localhost:8000/api/account/'

  export default {
    data() {
      return {
        clientBranchFields,
        inputFields,
        addList,
        queryUrl: apiUrl + 'client_branch/?',
        openDialog: false,
        accountData:[],
        clientBranchData: [],
      }
    },
    created() {
      this.fetchItems();
    },
    mounted() {
      this.searchClientBranch()
    },
    methods: {
      fetchItems() {
        axios.get(accountUrl)
          .then(response => {
            this.accountData = response.data;
          })
          .catch(error => {
            console.error(error);
          });
      },

      searchClientBranch: async function () {
        this.queryUrl = apiUrl + 'client_branch/?'
        clientBranchFields.forEach(field => {
          if(field.searchRef)
              this.queryUrl += field.name + '=' + field.searchRef + '&'
        })
        this.clientBranchData = (await axios.get(this.queryUrl)).data
      },
  
      fillInput: function (client_branch) {
        this.inputFields[0].inputRef = client_branch['client_id']
        axios.get(apiUrl + 'client/' + client_branch['client_id'] + '/')
          .then(response => this.inputFields[1].inputRef = response.data['name'])
  
        this.inputFields[2].inputRef = client_branch['branch_name']
  
        if(client_branch['account_id']) {
          this.inputFields[3].inputRef = client_branch['account_id']
          axios.get(apiUrl + 'account/' + client_branch['account_id'] + '/')
            .then(response => {
              this.inputFields[4].inputRef = response.data['currency_type']
              this.inputFields[5].inputRef = response.data['balance']
              this.inputFields[6].inputRef = response.data['interest_rate']
              this.inputFields[7].inputRef = response.data['staff_id']
              this.inputFields[8].inputRef = response.data['register_date']
            })
        }
        else for(let i = 3; i <= 8; i++) this.inputFields[i].inputRef = ''
      },
  
      openAccount: function () {
        this.openDialog = false
        let data = {}
        addList.forEach(i => data[inputFields[i].name] = inputFields[i].inputRef)
        axios.post(apiUrl + 'client_branch/open_account/', data)
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
                message: 'Fail: ' + error.response.data,
                type: 'error'
              })
            })
      },
  
      updateAccount: function () {
        if(!inputFields[3].inputRef){
          ElMessage({
            message: 'No account id',
            type: 'error'
          })
          return
        }
        let data = {}
        updateList.forEach(i => data[inputFields[i].name] = inputFields[i].inputRef)
        axios.put(apiUrl + 'account/' + inputFields[3].inputRef + '/', data)
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
                message: 'Fail: ' + error.response.data,
                type: 'error'
              })
          })
      },
  
      deleteAccount: function () {
        if(!inputFields[3].inputRef){
          ElMessage({
            message: 'No account id',
            type: 'error'
          })
          return
        }
        axios.delete(apiUrl + 'account/' + inputFields[3].inputRef + '/')
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
              message: 'Fail: ' + error.response.data,
              type: 'error'
            })
          })
      }
    }
  }
</script>
  