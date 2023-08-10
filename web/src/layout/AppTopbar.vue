<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useLayout } from '@/layout/composables/layout';
import { useRouter } from 'vue-router';
import axios from 'axios';

const { onMenuToggle } = useLayout();

const outsideClickListener = ref(null);
const topbarMenuActive = ref(false);
const router = useRouter();
const version = import.meta.env.VITE_APP_VERSION;

onMounted(() => {
    bindOutsideClickListener();
});

onBeforeUnmount(() => {
    unbindOutsideClickListener();
});

const onTopBarMenuButton = () => {
    topbarMenuActive.value = !topbarMenuActive.value;
};
// const onSettingsClick = () => {
//     topbarMenuActive.value = false;
//     router.push('/documentation');
// };
const topbarMenuClasses = computed(() => {
    return {
        'layout-topbar-menu-mobile-active': topbarMenuActive.value
    };
});

const bindOutsideClickListener = () => {
    if (!outsideClickListener.value) {
        outsideClickListener.value = (event) => {
            if (isOutsideClicked(event)) {
                topbarMenuActive.value = false;
            }
        };
        document.addEventListener('click', outsideClickListener.value);
    }
};
const unbindOutsideClickListener = () => {
    if (outsideClickListener.value) {
        document.removeEventListener('click', outsideClickListener);
        outsideClickListener.value = null;
    }
};
const isOutsideClicked = (event) => {
    if (!topbarMenuActive.value) return;

    const sidebarEl = document.querySelector('.layout-topbar-menu');
    const topbarEl = document.querySelector('.layout-topbar-menu-button');

    return !(sidebarEl.isSameNode(event.target) || sidebarEl.contains(event.target) || topbarEl.isSameNode(event.target) || topbarEl.contains(event.target));
};

const logout = () => {
    axios
        .get('/auth/slo')
        .then((res) => {
            const url = res.data
            window.location.href = url
        })
        .catch((err) => {
            console.log(err);
        });
};
</script>

<template>
    <div class="layout-topbar">
        <router-link to="/" class="layout-topbar-logo">
            <img src="@/assets/img/esun-ocr-logo.svg" alt="logo" />
            <div style="width: 400px; margin-left: 10px">
                <span style="width: 380px; color: #09747a">智能OCR服務</span>
                <h6  style="margin: 0;"> {{version}} </h6> 
            </div>
        </router-link>

        <button class="p-link layout-menu-button layout-topbar-button" @click="onMenuToggle()">
            <i class="pi pi-bars"></i>
        </button>

        <button class="p-link layout-topbar-menu-button layout-topbar-button" @click="onTopBarMenuButton()">
            <i class="pi pi-ellipsis-v"></i>
        </button>

        <div class="layout-topbar-menu" :class="topbarMenuClasses">
            <Button label="Logout" class="p-button-text p-button-rounded border-none font-light line-height-2 text-xl text-blue-500" @click="logout"></Button>
        </div>
    </div>
    
    <!-- <div id="pageWarpper">
        <div id="contentWarpper">
            <nav>標頭</nav>
            <div id="notifyMessageContainer">通知訊息</div>
            <div id="myFavoriteContainer">我的最愛</div>
            <div id="pageContentWarpper">
            <div id="mainDashboardContainer">個人導航板</div>
            <div id="systemContainer">系統連結地圖</div>
            </div>
        </div>
    </div> -->
</template>

<style lang="scss" scoped></style>
