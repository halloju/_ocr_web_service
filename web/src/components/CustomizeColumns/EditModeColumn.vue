<script>
import { defineComponent } from 'vue';
import Icon from '@/components/Icon.vue';
import { mapState, mapMutations } from 'vuex';

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
    emits: ['save', 'delete', 'click', 'complete'],
    methods: {
        handleDelete(scope) {
            this.$emit('delete', scope.row);
        },
        handleClick(index) {
            this.$emit('click', index);
        },
        handleChange(index, row) {
            var cond1 = row.annotation.title != undefined && row.annotation.title != '' && row.annotation.title != null;
            var cond2 = row.annotation.filters != null && row.annotation.filters.length > 0;
            if (cond1 && cond2) this.$emit('complete', index, true);
            else this.$emit('complete', index, false);
            this.$emit('save', index);
        }
    }
});
</script>

<template>
    <el-table-column v-if="buttonText" :label="buttonText" :min-width="40">
        <template v-slot="scope">
            <el-input :class="{ 'disabled-input': !scope.row.edited }" v-model="scope.row.annotation.title" @click="handleClick(scope.$index)" @change="handleChange(scope.$index, scope.row)">
                {{ scope.row.annotation.title }}
            </el-input>
        </template>
    </el-table-column>
    <el-table-column v-if="filterButtonText" :label="filterButtonText" :min-width="40">
        <template v-slot="scope">
            <el-select v-model="scope.row.annotation.filters" multiple @change="handleChange(scope.$index, scope.row)" placeholder="請選擇">
                <el-option v-for="item in option" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
        </template>
    </el-table-column>
    <el-table-column v-if="deleteColumnName" :label="deleteColumnName" :min-width="16">
        <template v-slot="scope">
            <a href="#" @click.prevent="handleDelete(scope)" title="Delete">
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