<script>
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'ViewEditResultColumn',
    props: {
        buttonText: {
            type: String,
            default: 'View'
        }
    }
});
</script>

<template>
    <el-table-column :label="buttonText" :min-width="45">
        <template v-slot="scope">
            <el-input v-model="scope.row.annotation.title" disabled>
                {{ scope.row.annotation.title }}
            </el-input>
        </template>
    </el-table-column>
</template>


