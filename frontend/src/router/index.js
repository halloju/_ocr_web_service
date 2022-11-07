import { createRouter, createWebHistory } from 'vue-router'
import LoginView from "@/views/LoginView.vue"
import Home from '@/views/Home.vue'
import Define from '@/views/Define.vue'
import DefineStep1 from '@/views/DefineStep1.vue'
import DefineStep2 from '@/views/DefineStep2.vue'
import DefineStep3 from '@/views/DefineStep3.vue'
import DefineStep4 from '@/views/DefineStep4.vue'
import DefineStep5 from '@/views/DefineStep5.vue'
import TemplateList from '@/views/TemplateList.vue'
import TemplateList1 from '@/views/TemplateList1.vue'
import TemplateList2 from '@/views/TemplateList2.vue'
import TemplateOcr from '@/views/TemplateOcr.vue'
import TemplateOcr1 from '@/views/TemplateOcr1.vue'
import TemplateOcr2 from '@/views/TemplateOcr2.vue'
import CommonOcr from '@/views/CommonOcr.vue'
import CommonOcr1 from '@/views/CommonOcr1.vue'
import CommonOcr2 from '@/views/CommonOcr2.vue'

const routes = [
  {
    path: '/login',
    name: 'LoginView',
    component: LoginView,
  },
//   {
//     path: '/',
//     name: 'MenuView',
//     component: MenuView,
//     meta: { requiresAuth: true },
//   },
  {
    path: '/',
    name: 'Home',
    component: Home,
    // meta: { requiresAuth: true },
  },
  {
    path: '/define',
    name: 'Define',
    component: Define,
    redirect: '/define/step1',
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
      },
      {
        path: 'step5',
        name: 'DefineStep5',
        component: DefineStep5,
      }
    ]
  },
  {
    path: '/template-list',
    name: 'TemplateList',
    component: TemplateList,
    redirect: '/template-list/private',
    // meta: { requiresAuth: true },
    children:[
      {
        path: 'private',
        name: 'TemplateList1',
        component: TemplateList1,
      },
      {
        path: 'public',
        name: 'TemplateList2',
        component: TemplateList2,
      }
    ]
  },
  {
    path: '/template-ocr',
    name: 'TemplateOcr',
    component: TemplateOcr,
    redirect: '/template-ocr/upload',
    // meta: { requiresAuth: true },
    children:[
      {
        path: 'upload',
        name: 'TemplateOcr1',
        component: TemplateOcr1,
      },
      {
        path: 'confirm',
        name: 'TemplateOcr2',
        component: TemplateOcr2,
      },
    ]
  },
  {
    path: '/common-ocr',
    name: 'CommonOcr',
    component: CommonOcr,
    redirect: '/common-ocr/upload',
    // meta: { requiresAuth: true },
    children:[
      {
        path: 'upload',
        name: 'CommonOcr1',
        component: CommonOcr1,
      },
      {
        path: 'confirm',
        name: 'CommonOcr2',
        component: CommonOcr2,
      },
    ]
  }
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
