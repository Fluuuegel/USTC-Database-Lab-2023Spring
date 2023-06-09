<template>
    <el-menu router 
      mode="horizontal" 
      :default-active="$route.path"  
    >
      <el-menu-item index="/admin/client">Client Management</el-menu-item>
      <el-menu-item index="/admin/account">Account Management</el-menu-item>
      <el-menu-item index="/admin/loan">Loan Management</el-menu-item>
      <el-menu-item index="/admin/statistics">Statistics</el-menu-item>
    </el-menu>
  </template>
  
  <script>
  export default {
    name: "AppHeader"
  }
  </script>