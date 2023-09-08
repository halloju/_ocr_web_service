<script>
export default {
    props: {
        label: {
            type: String,
            required: true
        },
        icon: {
            type: String,
            required: true
        },
        type: {
            type: String,
            required: true
        },
        handler: {
            type: String,
            required: true
        }
    },
    methods: {
        handleClick(templateId) {
            this.$emit(this.handler, templateId);
        }
    }
};
</script>

<template>
    <el-table-column :label="label" :min-width="10">
        <template #default="scope">
            <el-button size="" :type="type" plain @click="handleClick(scope.row.template_id)" :icon="icon" circle />
        </template>
    </el-table-column>
</template>
