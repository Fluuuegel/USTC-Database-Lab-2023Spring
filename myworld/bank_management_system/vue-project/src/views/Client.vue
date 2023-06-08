<template>
  <el-container>
    <el-main>
      <el-space wrap>
        <el-card class="box-card" style="width: 1025px">
          <el-table :data="clientData" style="width: 100%" max-height="430" height="430">
            <el-table-column fixed prop="id" label="Id" width="125" />
            <el-table-column prop="name" label="Name" width="125" />
            <el-table-column prop="phone_number" label="Phone Number" width="175" />
            <el-table-column prop="address" label="Address" width="250" />
            <el-table-column prop="contact_name" label="Contact Name" width="175" />
            <el-table-column prop="contact_phone_number" label="Contact Phone Number" width="200" />
            <el-table-column prop="contact_relationship" label="Contact Relationship" width="200">
            </el-table-column>
          </el-table>
        </el-card>

        <el-card class="box-card" style="width: 215px">
          <el-form>
            <el-form-item>
              <el-select v-model="selectedField" placeholder="Select Field">
                <el-option label="Id" value="id" />
                <el-option label="Name" value="name"/>
              </el-select>
            </el-form-item>
          </el-form>

          <el-form>
            <el-form-item>
              <el-input v-model="searchContent" placeholder="Search Content" />
            </el-form-item>
          </el-form>
          
          <el-button type="primary" @click="searchClient()">Search</el-button>
          <el-popconfirm
              title="Confirm to delete?"
              cancel-button-type="primary"
              cancel-button-text="No"
              confirm-button-type="danger"
              confirm-button-text="Yes"
              @confirm="deleteClient"
          >
            <template #reference>
              <el-button type="danger">Delete</el-button>
            </template>
          </el-popconfirm>
        </el-card>

        <el-card class="box-card" table-layout="auto" style="width: 800px;">
          <el-table :data="searchData" style="width: 100%" empty-text="No Data" max-height="132" height="132">
            <el-table-column fixed prop="id" label="Id" width="100" />
            <el-table-column prop="name" label="Name" width="100" />
            <el-table-column prop="phone_number" label="Phone Number" width="150" />
            <el-table-column prop="address" label="Address" width="125" />
            <el-table-column prop="contact_name" label="Contact Name" width="150" />
            <el-table-column prop="contact_phone_number" label="Contact Phone Number" width="200" />
            <el-table-column prop="contact_relationship" label="Contact Relationship" width="175">
          </el-table-column>
          </el-table>
        </el-card>
      </el-space>
    </el-main>

    <el-aside width="275px">
      <div style="min-height: 20px;"></div>
      <el-card class="box-card" style="width: 273px">
        <el-form
          label-position="top"
        >
          <el-form-item v-for="field in clientFields" :key="field.name" :label="field.label">
            <el-input v-model="field.inputRef" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="addClient">Add</el-button>
            <el-button type="warning">Update</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-aside>
  </el-container>
</template>

<script>
import axios from 'axios';
import {ElMessage} from 'element-plus'

const clientUrl = 'http://localhost:8000/api/client/'

const clientFields = [
  {'name': 'id', 'label': 'Id'},
  {'name': 'name', 'label': 'Name',},
  {'name': 'phone_number', 'label': 'Phone Number'},
  {'name': 'address', 'label': 'Address'},
  {'name': 'contact_name', 'label': 'Contact Name'},
  {'name': 'contact_phone_number', 'label': 'Contact Phone Number'},
  {'name': 'contact_relationship', 'label': 'Contact Relationship'}
]
clientFields.forEach(field => field['inputRef'] = '')

export default {
  data() {
    return {
      clientFields,
      clientData: [],
      selectedField: '',
      searchContent: '',
      queryUrl: '',
      searchData: [],
    };
  },
  created() {
    this.fetchItems();
  },
  methods: {
    fetchItems() {
      axios.get(clientUrl)
        .then(response => {
          this.clientData = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    searchClient() {
      if(this.selectedField === 'id') {
        this.searchData = this.clientData.filter(item => item.id === this.searchContent);
      }
      if(this.selectedField === 'name') {
        this.searchData = this.clientData.filter(item => item.name === this.searchContent);
      }
    },
    addClient() {
      let data = {}
      clientFields.forEach(field => data[field.name] = field.inputRef)
      axios.post(clientUrl, data)
        .then(response => {
          if(response.status === 201){
            ElMessage({
              message: 'Successfully added',
              type: 'success'
            })
          }
        })
        .catch(error => {
          console.log(error)
          ElMessage({
            message: 'Failed to add',
            type: 'error'
          })
        })
    },

    updateClient: function () {
      let data = {}
      clientFields.forEach(field => data[field.name] = field.inputRef)
      axios.put(clientUrl + clientFields[0].inputRef + '/', data)
        .then(response => {
          if(response.status === 200){
            ElMessage({
              message: 'Successfully updated',
              type: 'success'
            })
          }
        })
        .catch(error => {
          console.log(error)
          ElMessage({
            message: 'Failed to update',
            type: 'error'
          })
        })
    },

    deleteClient() {
      let deleteContent = this.searchContent
      axios.delete(clientUrl + deleteContent + '/')
        .then(response => {
          if(response.status === 204){
            ElMessage({
              message: 'Successfully deleted',
              type: 'success'
            })
          }
        })
        .catch(error => {
          console.log(error)
          ElMessage({
            message: 'Failed to delete',
            type: 'error'
          })
        })
    }
  }
};
</script>
