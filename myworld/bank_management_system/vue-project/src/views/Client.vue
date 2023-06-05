<template>
    <el-table :data="clientData" style="width: 100%">
    <el-table-column fixed prop="id" label="Id" width="150" />
    <el-table-column prop="name" label="Name" width="120" />
    <el-table-column prop="phone_number" label="Phone Number" width="120" />
    <el-table-column prop="address" label="Address" width="600" />
    <el-table-column prop="contact_name" label="Contact Name" width="120" />
    <el-table-column prop="contact_phone_number" label="Contact Phone Number" width="120" />
    <el-table-column prop="contact_relationship" label="Contact Relationship" width="120">
      <template #default>
        <el-button link type="primary" size="small" @click="handleClick"
          >Detail</el-button
        >
        <el-button link type="primary" size="small">Edit</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      clientData: [],
    };
  },
  created() {
    this.fetchItems();
  },
  methods: {
    fetchItems() {
      axios.get('http://localhost:8000/client')
        .then(response => {
          this.clientData = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
  },
};
</script>
