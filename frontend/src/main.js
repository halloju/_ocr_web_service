import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.css';
import BootstrapVue3 from 'bootstrap-vue-3'
import { createApp } from 'vue'
import store from './store'
import router from './router'
import App from './App.vue'

axios.defaults.withCredentials = false;
axios.defaults.crossDomain=true;
axios.defaults.baseURL="http://35.194.164.191:1313"
// axios.defaults.baseURL="http://localhost:5000"
// console.log(import.meta.env.VITE_BACKEND_HOST)

createApp(App)
.use(router, axios)
.use(store)
.use(BootstrapVue3)
.mount('#app')


export function resultShow(){
    $('.searchResult').show();
}

