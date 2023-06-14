<template>
  <el-row justify="center">
    <div class="demo-image">
      <div class="block">
        <span class="demonstration">{{ id }}</span>
        <el-image style="width: 100px; height: 100px" :src="imageUrl" fit="fit"/>
      </div>
    </div>
    <el-card class="box-card" style="width: 225px">
      <el-col>
        <div style="min-height: 50px;"></div>
        <input type="file" accept="image/*" style="width: 175px;" @change="handlePhotoUpload">
        <div style="min-height: 20px;"></div>
        <el-button type="primary" @click="uploadImage">Upload Image</el-button>
      </el-col>
    </el-card>
  </el-row>
  
  <el-row justify="space-around">
    <el-space warp>
      <el-card class="box-card" style="width: 1250px">
        <el-table :data="clientData" table-layout="auto">
          <el-table-column prop="id" label="ID"/>
          <el-table-column prop="name" label="Name"/>
          <el-table-column prop="phone_number" label="Phone Number"/>
          <el-table-column prop="address" label="Address" width="200" />
          <el-table-column prop="contact_name" label="Contact Name"/>
          <el-table-column prop="contact_phone_number" label="Contact Phone Number"/>
          <el-table-column prop="contact_relationship" label="Contact Relationship"/>
        </el-table>
      </el-card>
    </el-space>
  </el-row>
  <el-row justify="space-around">
    <el-space warp>
      <el-card class="box-card" style="width: 625px">
        <el-table :data="clientBranchData" table-layout="auto">
          <el-table-column prop="client_id" label="ID"/>
          <el-table-column prop="branch_name" label="Branch Name"/>
          <el-table-column prop="account_id" label="Account ID"/>
        </el-table>
      </el-card>
      <el-card class="box-card" style="width: 625px">
        <el-table :data="clientLoanData" table-layout="auto">
          <el-table-column prop="client_id" label="ID"/>
          <el-table-column prop="loan_id" label="Loan ID"/>
          <el-table-column prop="status" label="Status"/>
        </el-table>
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
    {'name': 'photo', 'label': 'Photo'}
  ]
  inputFields.forEach(field => field['inputRef'] = '')

  export default {
    name: "User",
    data() {
      return {
        inputFields,
        userData: [],
        clientData: [],
        clientBranchData: [],
        clientLoanData: [],
        userUrl: 'http://localhost:8000/register/user/?id=',
        clientUrl: 'http://localhost:8000/api/client_search/?id=',
        clientBranchUrl: 'http://localhost:8000/api/client_branch/?client_id=',
        clientLoanUrl: 'http://localhost:8000/api/client_loan/?client_id=',
        id: null,
        image: null,
        imageUrl: ''
      };
    },
    created() {
      this.id = this.$route.params.id;
      this.displayClient();
    },
    methods: {
      displayClient: async function () {
        this.userUrl += this.id + '&'
        this.userData = (await axios.get(this.userUrl)).data.filter(id=>id.id==this.id)
        this.clientUrl += this.id + '&'
        this.clientData = (await axios.get(this.clientUrl)).data
        this.clientBranchUrl += this.id + '&'
        this.clientBranchData = (await axios.get(this.clientBranchUrl)).data
        this.clientLoanUrl += this.id + '&'
        this.clientLoanData = (await axios.get(this.clientLoanUrl)).data
        this.imageUrl = this.userData[0].photo
      },
      handlePhotoUpload(event) {
        this.image = event.target.files[0];
      },
      uploadImage() {
        const formData = new FormData()
        formData.append('id', this.id)
        formData.append('image', this.image)
        axios.post('http://localhost:8000/register/user/uploadImage/', formData)
          .then(response => {
            ElMessage({
              message: 'Image uploaded successfully',
              type: 'success'
            })
          })
          .catch(error => {
            ElMessage({
              message: 'Image upload failed',
              type: 'error'
            })
          });
      }
    }
  }

</script>

<style scoped>
.demo-image .block {
  padding: 20px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  display: inline-block;
  width: 100%;
  box-sizing: border-box;
  vertical-align: top;
}
.demo-image .block:last-child {
  border-right: none;
}
.demo-image .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 10px;
}
</style>