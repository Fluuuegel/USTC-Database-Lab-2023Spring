import {createWebHistory, createRouter} from "vue-router";
import ClientManagement from "@/views/ClientManagement.vue";
import AccountManagement from "@/views/AccountManagement.vue";
import LoanManagement from "@/views/LoanManagement.vue";
import BusinessStatistics from "@/views/BusinessStatistics.vue";
import Register from "@/views/Register.vue";
import User from "@/views/User.vue";

const routes = [
    {
        path: "/",
        redirect: "/register",
    },
    {
        path: "/admin/client",
        name: "ClientManagement",
        component: ClientManagement
    },
    {
        path: "/admin/account",
        name: "AccountManagement",
        component: AccountManagement
    },
    {
        path: "/admin/loan",
        name: "LoanManagement",
        component: LoanManagement
    },
    {
        path: "/admin/statistics",
        name: "BusinessStatistics",
        component: BusinessStatistics
    },
    {
        path: "/register",
        name: "Register",
        component: Register
    },
    {
        path: "/user/:id",
        name: "User",
        component: User
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;