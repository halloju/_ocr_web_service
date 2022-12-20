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
                    path: '/features/general',
                    name: 'General1',
                    component: () => import('@/views/pages/features/General.vue')
                },
                {
                    path: '/features/self-define/step/1',
                    name: 'SelfDefine1',
                    component: () => import('@/views/pages/features/self-define/step1.vue')
                },
                {
                    path: '/features/self-define/step/2',
                    component: () => import('@/views/pages/features/self-define/step.vue'),
                    props: { Boxes: [{ name: 'recs_text', title: '文字辨識位置', step: 2, fillColor: { r: 0, g: 255, b: 0, a: 0.5 } }],
                             step: 2, pageTitle: '文字辨識位置', pageDesc: '請選擇文字辨識位置' }
                },
                {
                    path: '/features/self-define/step/3',
                    component: () => import('@/views/pages/features/self-define/step.vue'),
                    props: { Boxes: [{ name: 'recs_block', title: '核取方塊位置', step: 3, fillColor: { r: 0, g: 0, b: 255, a: 0.5 } }],
                             step: 3, pageTitle: '方塊位置', pageDesc: '請選擇方塊辨識位置' }
                },  
                {
                    path: '/features/self-define/step/4',
                    component: () => import('@/views/pages/features/self-define/step.vue'),
                    props: { Boxes: [{ name: 'recs_mask', title: '遮罩位置', step: 4, fillColor: { r: 0, g: 0, b: 0, a: 0.5 } }],
                             step: 4, pageTitle: '遮罩位置', pageDesc: '請選擇遮罩位置' }
                },
                {
                    path: '/features/self-define/step/5',
                    name: 'SelfDefine5',
                    component: () => import('@/views/pages/features/self-define/step.vue'),
                    props: {
                        Boxes: [
                            {
                                name: 'recs_text',
                                title: '文字辨識位置',
                                fillColor: {
                                    r: 0,
                                    g: 255,
                                    b: 0,
                                    a: 0.5
                                }
                            },
                            {
                                name: 'recs_block',
                                title: '核取方塊位置',
                                fillColor: {
                                    r: 0,
                                    g: 0,
                                    b: 255,
                                    a: 0.5
                                }
                            }
                        ]
                    },
                    step: 5
                },
                {
                    path: '/features/model-list/person',
                    name: 'Person',
                    component: () => import('@/views/pages/features/model-list/person.vue')
                },
                {
                    path: '/features/model-list/public',
                    name: 'Public',
                    component: () => import('@/views/pages/features/model-list/public.vue')
                },
                {
                    path: '/uikit/formlayout',
                    name: 'formlayout',
                    component: () => import('@/views/uikit/FormLayout.vue')
                },
                {
                    path: '/uikit/input',
                    name: 'input',
                    component: () => import('@/views/uikit/Input.vue')
                },
                {
                    path: '/uikit/floatlabel',
                    name: 'floatlabel',
                    component: () => import('@/views/uikit/FloatLabel.vue')
                },
                {
                    path: '/uikit/invalidstate',
                    name: 'invalidstate',
                    component: () => import('@/views/uikit/InvalidState.vue')
                },
                {
                    path: '/uikit/button',
                    name: 'button',
                    component: () => import('@/views/uikit/Button.vue')
                },
                {
                    path: '/uikit/table',
                    name: 'table',
                    component: () => import('@/views/uikit/Table.vue')
                },
                {
                    path: '/uikit/list',
                    name: 'list',
                    component: () => import('@/views/uikit/List.vue')
                },
                {
                    path: '/uikit/tree',
                    name: 'tree',
                    component: () => import('@/views/uikit/Tree.vue')
                },
                {
                    path: '/uikit/panel',
                    name: 'panel',
                    component: () => import('@/views/uikit/Panels.vue')
                },

                {
                    path: '/uikit/overlay',
                    name: 'overlay',
                    component: () => import('@/views/uikit/Overlay.vue')
                },
                {
                    path: '/uikit/media',
                    name: 'media',
                    component: () => import('@/views/uikit/Media.vue')
                },
                {
                    path: '/uikit/menu',
                    component: () => import('@/views/uikit/Menu.vue'),
                    children: [
                        {
                            path: '/uikit/menu',
                            component: () => import('@/views/uikit/menu/PersonalDemo.vue')
                        },
                        {
                            path: '/uikit/menu/seat',
                            component: () => import('@/views/uikit/menu/SeatDemo.vue')
                        },
                        {
                            path: '/uikit/menu/payment',
                            component: () => import('@/views/uikit/menu/PaymentDemo.vue')
                        },
                        {
                            path: '/uikit/menu/confirmation',
                            component: () => import('@/views/uikit/menu/ConfirmationDemo.vue')
                        }
                    ]
                },
                {
                    path: '/uikit/message',
                    name: 'message',
                    component: () => import('@/views/uikit/Messages.vue')
                },
                {
                    path: '/uikit/file',
                    name: 'file',
                    component: () => import('@/views/uikit/File.vue')
                },
                {
                    path: '/uikit/charts',
                    name: 'charts',
                    component: () => import('@/views/uikit/Chart.vue')
                },
                {
                    path: '/uikit/misc',
                    name: 'misc',
                    component: () => import('@/views/uikit/Misc.vue')
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
                    path: '/pages/timeline',
                    name: 'timeline',
                    component: () => import('@/views/pages/Timeline.vue')
                },
                {
                    path: '/pages/empty',
                    name: 'empty',
                    component: () => import('@/views/pages/Empty.vue')
                },
                {
                    path: '/pages/crud',
                    name: 'crud',
                    component: () => import('@/views/pages/Crud.vue')
                },
                {
                    path: '/documentation',
                    name: 'documentation',
                    component: () => import('@/views/utilities/Documentation.vue')
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
