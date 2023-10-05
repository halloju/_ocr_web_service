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
            default: null
        },
        filterButtonText: {
            type: String,
            default: null
        },
        checkColumnName: {
            type: String,
            default: null
        },
        deleteColumnName: {
            type: String,
            default: null
        },
        option: {
            type: Array(),
            default: []
        }
    },
    data() {
        return {
            clickedRows: []
        }
    },
    emits: ['save', 'delete', 'click'],
    methods: {
        handleSave(index) {
            this.$emit('save', index);
            if (!this.clickedRows.includes(index)) {
                this.clickedRows.push(index);
            }
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
    <el-table-column v-if="buttonText" :label="buttonText" :min-width="40">
        <template v-slot="scope">
            <el-input :class="{ 'disabled-input': !scope.row.edited }" v-model="scope.row.annotation.title" @click="handleClick(scope.$index)">
                {{ scope.row.annotation.title }}
            </el-input>
        </template>
    </el-table-column>
    <el-table-column v-if="filterButtonText" :label="filterButtonText" :min-width="40">
        <template v-slot="scope">
            <el-select v-model="scope.row.annotation.filters" multiple placeholder="請選擇">
                <el-option v-for="item in option" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
        </template>
    </el-table-column>
    <el-table-column v-if="checkColumnName" :label="checkColumnName" :min-width="15">
        <template v-slot="scope">
            <el-button type="default" @click="handleSave(scope.$index)" :class="{ 'clicked-color': clickedRows.includes(scope.$index)}"> V </el-button>
        </template>
    </el-table-column>
    <el-table-column v-if="deleteColumnName" :label="deleteColumnName" :min-width="15">
        <template v-slot="scope">
            <a href="#" @click.prevent="handleDelete(scope.row)" title="Delete">
                <icon type="delete-shape" fill="red" />
            </a>
        </template>
    </el-table-column>
</template>

<style scoped>
.clicked-color{
    background-color: #bcced3;
}
</style>