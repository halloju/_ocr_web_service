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
        checkColumnName: {
            type: String,
            default: 'Save'
        },
        deleteColumnName: {
            type: String,
            default: 'Delete'
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
    <el-table-column :label="buttonText" :min-width="45">
        <template v-slot="scope">
            <el-input :class="{ 'disabled-input': !scope.row.edited }" v-model="scope.row.annotation.title" @click="handleClick(scope.$index)">
                {{ scope.row.annotation.title }}
            </el-input>
        </template>
    </el-table-column>
    <el-table-column :label="checkColumnName" :min-width="20">
        <template v-slot="scope">
            <el-button type="default" @click="handleSave(scope.$index)"> 確認 </el-button>
        </template>
    </el-table-column>
    <el-table-column :label="deleteColumnName" :min-width="20">
        <template v-slot="scope">
            <a href="#" @click.prevent="handleDelete(scope.row)" title="Delete">
                <icon type="delete-shape" fill="red" />
            </a>
        </template>
    </el-table-column>
</template>
