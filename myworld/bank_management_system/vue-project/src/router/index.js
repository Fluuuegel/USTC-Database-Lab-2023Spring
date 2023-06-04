import {createWebHistory, createRouter} from "vue-router";
import Client from "@/views/Client.vue";

const routes = [
    {
        path: "/",
        redirect: "/client",
    },
    {
        path: "/client",
        name: "Client",
        component: Client
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;