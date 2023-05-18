/* eslint-disable prettier/prettier */
import { createRouter, createWebHashHistory } from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: '/home',
            component: AppLayout,
            children: [
                {
                    path: '/home',
                    name: 'dashboard',
                    component: () => import('@/views/Dashboard.vue')
                },
                {
                    path: '/features/ocr/:type',
                    name: 'OCR',
                    component: () => import('@/views/pages/features/OCR.vue')
                },
                {
                    path: '/features/general/model-list',
                    name: 'ModelList',
                    component: () => import('@/views/pages/features/template/ModelList.vue')
                },
                {
                    path: '/features/general/self-define/step',
                    name: 'SelfDefine',
                    component: () => import('@/views/pages/features/template/step.vue')
                },
                {
                    path: '/features/pdf2image',
                    name: 'pdf2image',
                    component: () => import('@/views/pages/features/pdf2image.vue')
                },
                {
                    path: '/blocks',
                    name: 'blocks',
                    component: () => import('@/views/utilities/Blocks.vue')
                },
                {
                    path: '/utilities/icons',
                    name: 'icons',
                    component: () => import('@/views/utilities/Icons.vue')
                },
                {
                    path: '/pages/empty',
                    name: 'empty',
                    component: () => import('@/views/pages/Empty.vue')
                },
                {
                    path: '/pages/crud',
                    name: 'crud',
                    component: () => import('@/views/pages/features/template/Crud.vue')
                }
            ]
        },
        {
            path: '/',
            name: 'landing',
            component: () => import('@/views/pages/Landing.vue')
        },
        {
            path: '/pages/notfound',
            name: 'notfound',
            component: () => import('@/views/pages/NotFound.vue')
        },

        {
            path: '/auth/login',
            name: 'login',
            component: () => import('@/views/pages/auth/Login.vue')
        },
        {
            path: '/auth/access',
            name: 'accessDenied',
            component: () => import('@/views/pages/auth/Access.vue')
        },
        {
            path: '/auth/error',
            name: 'error',
            component: () => import('@/views/pages/auth/Error.vue')
        }
    ]
});

export default router;
