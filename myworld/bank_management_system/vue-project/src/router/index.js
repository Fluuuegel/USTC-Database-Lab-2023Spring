import {createWebHistory, createRouter} from "vue-router";
import Customer from "@/views/Customer";

const routes = [
    {
        path: "/",
        redirect: "/customer",
    },
    {
        path: "/customer",
        name: "Customer",
        component: Customer
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;