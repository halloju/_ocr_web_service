<script>
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'ViewRecognitionResultColumn',
    props: {
        buttonText: {
            type: String,
            default: 'Recognition Result'
        },
        checkColumnName: {
            type: String,
            default: 'Confirm'
        }
    },
    emits: ['save', 'click'],
    methods: {
        handleSave(index) {
            this.$emit('save', index);
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
            <el-input :class="{ 'disabled-input': !scope.row.edited }" v-model="scope.row.annotation.text" @click="handleClick(scope.$index)">
                {{ scope.row.annotation.text }}
            </el-input>
        </template>
    </el-table-column>

    <el-table-column :label="checkColumnName" :min-width="20">
        <template v-slot="scope">
            <el-button type="default" @click="handleSave(scope.$index)"> 確認 </el-button>
        </template>
    </el-table-column>
</template>
