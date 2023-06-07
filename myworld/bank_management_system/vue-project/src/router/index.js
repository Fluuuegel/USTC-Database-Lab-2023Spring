import {createWebHistory, createRouter} from "vue-router";
import Client from "@/views/Client.vue";
import Account from "@/views/Account.vue";

const routes = [
    {
        path: "/",
        redirect: "/client",
    },
    {
        path: "/client",
        name: "Client",
        component: Client
    },
    {
        path: "/account",
        name: "Account",
        component: Account
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;