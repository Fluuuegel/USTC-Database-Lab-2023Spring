<template>
    <el-row justify="space-around">
  
      <el-col :span="5">
        <el-form
          label-position="left"
          label-width="110px"
          size="small"
        >
          <el-form-item v-for="field in clientBranchFields" :key="field.name" :label="field.label">
            <el-input v-model="field.searchRef"/>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="searchSavingAccount">查询</el-button>
          </el-form-item>
        </el-form>
      </el-col>
  
      <el-col :span="8">
        <div class="pagination-block">
          <el-table :data="info.results" border @row-click="fillInput" size="small">
            <el-table-column prop="client_id" label="身份证号"/>
            <el-table-column prop="branch_name" label="支行名"/>
            <el-table-column prop="account_id" label="储蓄账户号"/>
          </el-table>
        </div>
      </el-col>
  
      <el-col :span="9">
        <el-form
          label-position="left"
          label-width="110px"
          size="small"
        >
          <el-form-item v-for="field in inputFields" :key="field.name" :label="field.label">
            <el-input v-model="field.inputRef"/>
          </el-form-item>
          <el-form-item>
            <el-dialog
              v-model="openDialog"
              title="开户确认"
              width="30%"
            >
              <span>
                <el-descriptions :column="1" border>
                  <el-descriptions-item v-for="i in add_indices" :label="inputFields[i].label"
                                        :key="inputFields[i].name" width="110px">
                    {{ inputFields[i].inputRef }}
                  </el-descriptions-item>
                </el-descriptions>
              </span>
              <template #footer>
                <span class="dialog-footer">
                  <el-button @click="openDialog = false">取消</el-button>
                  <el-button type="primary" @click="openSavingAccount">确认</el-button>
                </span>
              </template>
            </el-dialog>
            <el-button type="success" @click="openDialog = true">开户</el-button>
            <el-button type="warning" @click="updateSavingAccount">更新</el-button>
            <el-popconfirm
              :title="'确认要删除储蓄账户' + inputFields[3].inputRef + '吗？'"
              cancel-button-type="primary"
              cancel-button-text="否"
              confirm-button-type="danger"
              confirm-button-text="是"
              @confirm="deleteSavingAccount"
            >
              <template #reference>
                <el-button type="danger">销户</el-button>
              </template>
            </el-popconfirm>
          </el-form-item>
        </el-form>
      </el-col>
  
    </el-row>
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
    {'name': 'currency', 'label': 'Currency Type'},
    {'name': 'balance', 'label': 'Balance'},
    {'name': 'interest_rate', 'label': 'Interest Rate'},
    {'name': 'staff_id', 'label': 'Staff ID'},
    {'name': 'register_date', 'label': 'Register Date'},
  ]
  inputFields.forEach(field => field['inputRef'] = '')

  const add_indices = [0, 2, 4, 6, 7]
  const update_indices = [3, 4, 5, 6, 7]
  
  const apiUrl = 'http://localhost:8000/api/'
  
  const auth_config = {auth: {username: 'tanix', password: '1234'}}
  
  export default {
    name: "SavingAccountManagement",
    data() {
      return {
        clientBranchFields,
        inputFields,
        add_indices,
        info: '',
        queryUrl: apiUrl + 'client_branch/?',
        openDialog: false,
      }
    },
    mounted() {
      this.searchSavingAccount()
    },
    methods: {

      searchSavingAccount: async function () {
        let vm = this
        vm.queryUrl = apiUrl + 'client_branch/?'
        clientBranchFields.forEach(field => {
          if(field.searchRef)
              vm.queryUrl += field.name + '=' + field.searchRef + '&'
        })
        vm.info = (await axios.get(vm.queryUrl)).data
        this.pageCount = Math.ceil(this.info.count / 8)
      },
  
      fillInput: function (client_branch) {
        let vm = this
        vm.inputFields[0].inputRef = client_branch['client_id']
        axios.get(apiUrl + 'client/' + client_branch['client_id'] + '/')
          .then(response => vm.inputFields[1].inputRef = response.data['name'])
  
        vm.inputFields[2].inputRef = client_branch['branch_name']
  
        if(client_branch['account_id']){
          vm.inputFields[3].inputRef = client_branch['account_id']
          axios.get(apiUrl + 'account/' + client_branch['account_id'] + '/')
            .then(response => {
              vm.inputFields[4].inputRef = response.data['currency']
              vm.inputFields[5].inputRef = response.data['balance']
              vm.inputFields[6].inputRef = response.data['interest_rate']
              vm.inputFields[7].inputRef = response.data['staff_id']
              vm.inputFields[8].inputRef = response.data['open_date']
            })
        }
        else for(let i = 3; i <= 9; i++) vm.inputFields[i].inputRef = ''
      },
  
      openSavingAccount: function () {
        this.openDialog = false
        let data = {}
        add_indices.forEach(i => data[inputFields[i].name] = inputFields[i].inputRef)
        axios.post(apiUrl + 'client_branch/open_account/', data)
            .then(response => {
              if(response.status === 201){
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
  
      updateSavingAccount: function () {
        if(!inputFields[3].inputRef){
          ElMessage({
            message: 'No account id',
            type: 'error'
          })
          return
        }
        let data = {}
        update_indices.forEach(i => data[inputFields[i].name] = inputFields[i].inputRef)
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
  