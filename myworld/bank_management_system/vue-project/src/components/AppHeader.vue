<template>
    <el-menu router 
      mode="horizontal" 
      :default-active="$route.path"  
    >
      <el-menu-item index="/client">Client Management</el-menu-item>
      <el-menu-item index="/account">Account Management</el-menu-item>
      <el-menu-item index="/loan">Loan Management</el-menu-item>
      <el-menu-item index="/statistics">Statistics</el-menu-item>
    </el-menu>
  </template>
  
  <script>
  export default {
    name: "AppHeader"
  }
  </script>