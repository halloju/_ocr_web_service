/* eslint-disable prettier/prettier */
import { createRouter, createWebHistory } from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';
import axios from 'axios';
import { AUTH_URL } from '@/url.js';

const router = createRouter({
    history: createWebHistory(),
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
                    path: '/utilities/icons',
                    name: 'icons',
                    component: () => import('@/views/utilities/Icons.vue')
                },
                {
                    path: '/pages/empty',
                    name: 'empty',
                    component: () => import('@/views/pages/Empty.vue')
                },
                // {
                //     path: '/pages/crud',
                //     name: 'crud',
                //     component: () => import('@/views/pages/features/template/Crud.vue')
                // }
            ],
            meta: { requiresAuth: true } // This route requires authentication
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

router.beforeEach(async (to, from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

    // Call the backend route to check if the user is authenticated
    try {
        const response = await axios.get(AUTH_URL)
        const isAuthenticated = response.data.isAuthenticated;

        if (requiresAuth && !isAuthenticated) {
            next('/auth/login');
        } else {
            next();
        }
    } catch (error) {
        console.error(error);
        next('/auth/login');
    }
})

export default router;
