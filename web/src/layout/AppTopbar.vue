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
            const url = res.data;
            window.location.href = url;
            this.$router.push('/');
        })
        .catch((err) => {
            console.log(err);
        });
};
</script>

<template>
    <nav style="width: calc(100% + 10px)">
        <div id="navPageLogo">
            <a href="/"><img src="/esun_images/logo_white_esun.svg" title="玉山銀行E.SUN Bank" /></a>
        </div>
        <div id="navPageTitle">｜智能OCR服務</div>

        <div id="navFunctionContainer">
            <div class="navFunction iconBtn" id="navLogoutContainer">
                <button class="uiStyle sizeS" id="btnNavLogout" @click="logout"></button>
            </div>
        </div>
    </nav>
</template>

<style lang="scss" scoped></style>
