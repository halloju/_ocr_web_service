<script setup>
import { useLayout } from '@/layout/composables/layout';

const { layoutConfig, contextPath } = useLayout();


</script>

<template>
    <div class="layout-footer">
        <span> 如有網頁相關問題請聯絡智金處 李立晟 (lilicheng-18440@esunbank.com)、侯貫中 (jerryhou-22095@esunbank.com)</span>
    </div>
</template>
<style lang="scss" scoped>
.layout-footer {
    position: fixed;
    width: 100%;
    padding: 0;
    height: 20px;
    font-size: 12px;
    background-color: rgb(234, 234, 234);
    bottom: 0;
}
</style>