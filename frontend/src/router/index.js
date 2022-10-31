import { createRouter, createWebHistory } from 'vue-router'
import Define from '@/views/Define.vue'
import DefineStep1 from '@/views/DefineStep1.vue'
import DefineStep2 from '@/views/DefineStep2.vue'
import DefineStep3 from '@/views/DefineStep3.vue'
import DefineStep4 from '@/views/DefineStep4.vue'

const routes = [
//   {
//     path: '/login',
//     name: 'LoginView',
//     component: LoginView,
//   },
//   {
//     path: '/',
//     name: 'MenuView',
//     component: MenuView,
//     meta: { requiresAuth: true },
//   },
  {
    path: '/define',
    name: 'Define',
    component: Define,
    // meta: { requiresAuth: true },
    children:[
      {
        path: 'step1',
        name: 'DefineStep1',
        component: DefineStep1,
      },
      {
        path: 'step2',
        name: 'DefineStep2',
        component: DefineStep2,
      },
      {
        path: 'step3',
        name: 'DefineStep3',
        component: DefineStep3,
      },
      {
        path: 'step4',
        name: 'DefineStep4',
        component: DefineStep4,
      }
    ]
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// router.beforeEach((to, from, next) => {
//   // 讀取一開始於Login寫入的Token
//   const token = store.state.token;
  
//   // 有token又到登入頁，就導向HomePage
//   if (to.name === 'LoginView' && token) {
//     next({ name: 'MenuView' })
//   }
//   else if (to.name === 'HomeView' && token){
//     next({ name: 'SingView' })
//   }
//   // 判斷有要求權限的頁面檢查token
//   else if (to.matched.some(res => res.meta.requiresAuth)) {
//     if(!token){
//         next({ name: 'LoginView' })
//     }
//     else {
//       next()
//     }
//   } 
//   else {
//     next()
//   }
// })

export default router
