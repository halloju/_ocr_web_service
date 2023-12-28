<script>
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'ViewEditResultColumn',
    props: {
        buttonText: {
            type: String,
            default: 'View'
        },
        filterButtonText: {
            type: String,
            default: 'View'
        },
        Names: {
            type: Object,
            required: true
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
    <el-table-column :label="filterButtonText" :min-width="40">
        <template v-slot="scope">
            <el-select v-model="scope.row.annotation.filters" multiple disabled>
                <el-option
                    v-for="(label, key) in Names" 
                    :key="key" 
                    :label="label" 
                    :value="key">
                    </el-option>
            </el-select>
        </template>
    </el-table-column>
</template>


