<script>
export default {
    props: {
        item: {
            type: Object,
            required: true
        },
        row: {
            type: Object,
            required: true
        }
    }
};
</script>

<template>
    <div v-if="item.editable || row.editable" class="editable-row">
        <el-input v-if="item.type === 'input'" size="small" v-model="row[item.prop]" :placeholder="`請輸入 ${item.label}`" @change="$emit('edit')" />
    </div>
    <div v-else class="editable-row">
        <span class="editable-row-span">{{ row[item.prop] }}</span>
    </div>
</template>

<style scoped>
/* Add any specific styles for the editable row here */
</style>
