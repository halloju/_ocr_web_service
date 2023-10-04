<script>
import { defineComponent } from 'vue';
import Icon from '@/components/Icon.vue';

export default defineComponent({
    components: {
        Icon
    },
    name: 'EditModeColumn',
    props: {
        buttonText: {
            type: String,
            default: 'Edit'
        },
        filterButtonText: {
            type: String,
            default: 'Edit'
        },
        checkColumnName: {
            type: String,
            default: 'Save'
        },
        deleteColumnName: {
            type: String,
            default: 'Delete'
        },
        option: {
            type: Array(),
            default: []
        }
    },
    emits: ['save', 'delete', 'click'],
    methods: {
        handleSave(index) {
            this.$emit('save', index);
        },
        handleDelete(row) {
            this.$emit('delete', row);
        },
        handleClick(index) {
            this.$emit('click', index);
        }
    }
});
</script>

<template>
    <el-table-column :label="buttonText" :min-width="40">
        <template v-slot="scope">
            <el-input :class="{ 'disabled-input': !scope.row.edited }" v-model="scope.row.annotation.title" @click="handleClick(scope.$index)">
                {{ scope.row.annotation.title }}
            </el-input>
        </template>
    </el-table-column>
    <el-table-column :label="filterButtonText" :min-width="40">
        <template v-slot="scope">
            <el-select v-model="scope.row.annotation.filters" multiple placeholder="請選擇">
                <el-option v-for="item in option" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
        </template>
    </el-table-column>
    <el-table-column :label="checkColumnName" :min-width="15">
        <template v-slot="scope">
            <el-button type="default" @click="handleSave(scope.$index)"> V </el-button>
        </template>
    </el-table-column>
    <el-table-column :label="deleteColumnName" :min-width="15">
        <template v-slot="scope">
            <a href="#" @click.prevent="handleDelete(scope.row)" title="Delete">
                <icon type="delete-shape" fill="red" />
            </a>
        </template>
    </el-table-column>
</template>
