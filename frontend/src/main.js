import axios from 'axios';
import { createApp } from 'vue'
import store from './store'
import { createRouter, createWebHistory } from 'vue-router'
import $ from "jquery"
import { Fancybox } from "@fancyapps/ui";
import "@fancyapps/ui/dist/fancybox.css";
import App from './App.vue'
import Home from '@/views/Home.vue'
import Question from '@/views/Question.vue'
import Confirm from '@/views/Confirm.vue'
import Market from '@/views/Market.vue'
import Analyzing from '@/views/Analyzing.vue'
import Result from '@/views/Result.vue'
import Quiz from '@/views/Quiz.vue'
import QuizResult from '@/views/QuizResult.vue'


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/', name: 'Home', component: Home},
        {path: '/question', name: 'Question', component: Question},
        {path: '/confirm', name: 'Confirm', component: Confirm},
        {path: '/market', name: 'Market', component: Market},
        {path: '/analyzing', name: 'Analyzing', component: Analyzing},
        {path: '/result', name: 'Result', component: Result},
        {path: '/quiz', name: 'Quiz', component: Quiz},
        {path: '/quizResult', name: 'QuizResult', component: QuizResult}
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

