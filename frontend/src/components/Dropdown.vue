<template>
<div class="menu-item" @click="isOpen = !isOpen">
    <img :src="img_src"/>
    <a href="#" class="menu-title">
        <p>{{ title }}</p>
    </a>
    <transition name="fade" appear>
        <div class="sub-menu" v-if="isOpen">
            <div v-for="(item, i) in items" :key="i" class="menu-item">
                <router-link :to="item.link">
                    <div class="link-container">
                        <p>{{item.title}}</p>
                    </div>
                </router-link>
            </div>
        </div>
    </transition>
</div>
</template>

<script>
export default {
    name: 'dropdown',
    props: ['title', 'items', 'img_src'],
    data () {
        return {
            isOpen: false
        }
    }
}
</script>

<style>
.navbar a {
    margin-left: 10px;
}
.navbar .menu-item svg {
    width: 10px;
    margin-left: 10px;
}
.navbar .menu-item .sub-menu {
    position: absolute;
    background-color: #222;
    top: calc(100% + 18px);
    left: 50%;
    transform: translateX(-50%);
    width: max-content;
    border-radius: 0px 0px 16px 16px;
}
.navbar .menu-item .sub-menu .link-container p {
    color: white;
}
.fade-enter-active,
.fade-leave-active {
    transition: all .5s ease-out;
}
.fade-enter,
.fade-leave-to {
    opacity: 0;
}
</style>