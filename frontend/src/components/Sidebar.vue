<template>
    <div class="sidebar">
        <div class="sidebarImg">
            <img :src="img_src"/>
        </div> 
        <div class="title">
            {{model}}
        </div>
        <div class="menu-items">
            <router-link :to="item.path" active-class="active" tag="button" exact :class="{disabled:  !(item.order <= parseInt(this.$route.name.slice(-1)))}" class="side-btn" v-for="(item, i) in model_bar">
                <div class="link-container">
                    <p>{{item.title}}</p>
                </div>
            </router-link>
        </div>
    </div>
</template>

<script>
export default {
    name: 'sidebar',
    props: {
        model: {
            type: String
        },
        img_src: {
            type: String
        },
        model_bar: {
            type: Object
        },
    },
    data() {
    },
    computed: {
        isDisabled() {
            if (parseInt(this.$route.name.slice(-1))!=='NaN') {
                return !(item.order <= parseInt(this.$route.name.slice(-1)))
            } else {
                return
            }
        }
    }
}
</script>

<style scoped>
@import '@/assets/css/sidebar.css';
</style>