<script>
export default {
    props: {
        items: {
            type: Array,
            required: true
        }
    }
};
</script>

<template>
    <div class="breadcrumbContainer">
        <ul>
            <li v-for="item in items" :key="item.label" :class="{ now: item.isCurrent }">
                <router-link v-if="item.path" :to="{ path: item.path }">{{ item.label }}</router-link>
                <span v-else>{{ item.label }}</span>
            </li>
        </ul>
    </div>
</template>

<style scoped>
/* Add any specific styles for the breadcrumb here */
</style>
