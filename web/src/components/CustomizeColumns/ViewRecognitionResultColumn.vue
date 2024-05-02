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
        handleSave(index, updatedText) {
            console.log('change:', updatedText);
            this.$emit('save', index, updatedText);
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
            <el-input :class="{ 'disabled-input': !scope.row.edited }" v-model="scope.row.annotation.text" @click="handleClick(scope.$index)" @change="handleSave(scope.$index, scope.row.annotation.text)">
                {{ scope.row.annotation.text }}
            </el-input>
        </template>
    </el-table-column>
</template>
