import axios from 'axios';
import { createApp } from 'vue'
import store from './store'
import { createRouter, createWebHistory } from 'vue-router'
import $ from "jquery"
import App from './App.vue'
import Home from '@/views/Home.vue'


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/', name: 'Home', component: Home},
    ],
    scrollBehavior(to, from, savedPosition) {
        // always scroll to top
        return { top: 0 }
    },
})

axios.defaults.withCredentials = false;
axios.defaults.crossDomain=true;
axios.defaults.baseURL="http://35.194.164.191:1313"
// axios.defaults.baseURL="http://localhost:5000"
// console.log(import.meta.env.VITE_BACKEND_HOST)

createApp(App)
.use(router, axios)
.use(store)
.mount('#app')


export function resultShow(){
    $('.searchResult').show();
}

