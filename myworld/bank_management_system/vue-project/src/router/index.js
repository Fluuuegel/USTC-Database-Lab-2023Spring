import {createWebHistory, createRouter} from "vue-router";
import ClientManagement from "@/views/ClientManagement.vue";
import AccountManagement from "@/views/AccountManagement.vue";
import LoanManagement from "@/views/LoanManagement.vue";
import BusinessStatistics from "@/views/BusinessStatistics.vue";

const routes = [
    {
        path: "/",
        redirect: "/client",
    },
    {
        path: "/client",
        name: "ClientManagement",
        component: ClientManagement
    },
    {
        path: "/account",
        name: "AccountManagement",
        component: AccountManagement
    },
    {
        path: "/loan",
        name: "LoanManagement",
        component: LoanManagement
    },
    {
        path: "/statistics",
        name: "BusinessStatistics",
        component: BusinessStatistics
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;