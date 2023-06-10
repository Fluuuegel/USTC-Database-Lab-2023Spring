<template>
  <el-row justify="space-around">
    <div style="min-height: 25px">The Great Bank</div>
  </el-row>
  <el-row justify="space-around">
    <el-space warp>
      <el-card class="box-card">
        <el-form label-position="left" label-width="75px">
          <el-form-item v-for="field in inputFields" :key="field.name" :label="field.label">
            <el-input v-model="field.inputRef" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="login">Login</el-button>
            <el-button type="primary" @click="register">Register</el-button>
            <el-button type="warning" @click="adminLogin">Admin Login</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-space>
  </el-row>
</template>

<script>
import axios from "axios"
import {ElMessage} from "element-plus"

const inputFields = [
  {'name': 'id', 'label': 'ID'},
  {'name': 'passwd', 'label': 'Password'},
]

inputFields.forEach(field => field['inputRef'] = '')

export default {
  data() {
    return {
      inputFields,
    }
  },
  methods: {
    login() {
      let data = {}
      inputFields.forEach(field => data[field.name] = field.inputRef)
      axios.post('http://localhost:8000/register/user/login/', data)
        .then(response => {
          if(response.status === 200) {
            ElMessage({
              message: 'Success',
              type: 'success'
            })
            this.$router.push(`/user/${data.id}`)
          }
        })
        .catch(error => {
          console.log(error)
          ElMessage({
            message: 'Failed to login',
            type: 'error'
          })
        })
    },

    register() {
      let data = {}
      axios.post('http://localhost:8000/register/user/register/', data)
        .then(response => {
          if(response.status === 201) {
            ElMessage({
              message: 'Success',
              type: 'success'
            })
            this.$router.push(`/user/${data.id}`)
          }
        })
        .catch(error => {
          console.log(error)
          ElMessage({
            message: 'Failed to register',
            type: 'error'
          })
        })
    },

  adminLogin() {
    this.$router.push(`/admin/client`)
  }
  }
}

</script>