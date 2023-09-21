<script>
import Nl2br from 'vue3-nl2br';
import Icon from '@/components/Icon.vue';

export default {
    components: {
        Icon,
        Nl2br
    },
    props: {
        shapes: {
            type: Array
        },
        editMode: {
            type: Boolean
        },
        selectedShapeName: {
            type: String
        },
        currentHoverShape: {
            type: String
        },
        justShow: {
            type: Boolean,
            default: false
        },
        rectangleType: {
            type: String
        },
        delete_shape: {
            type: Boolean
        },
        hasTitle: {
            type: Boolean
        }
    },
    data() {
        return {
            submit: '確認',
            // form data as copy
            formData: [],
            buttonText: this.editMode ? '欄位命名' : '欄位',
            buttonTitle: this.justShow ? '區塊類型' : 'index',
            titleColumnName: '欄位名稱'
            // shouldBeDisabled: false
        };
    },
    created() {
        if (this.shapes) {
            this.formData = this.shapes;
        }
    },
    computed: {
        showFormColumn() {
            return this.rectangleType !== 'mask';
        },
        showSaveButton() {
            return (this.rectangleType !== 'mask' && this.editMode) || !this.justShow;
        }
    },
    methods: {
        handleMouseEnter(shape) {
            this.$emit('sidebar-entry-enter', shape.name);
        },
        handleMouseLeave(shape) {
            this.$emit('sidebar-entry-leave', shape.name);
        },
        deleteShape(shape) {
            this.$emit('sidebar-entry-delete', shape.name);
        },
        submitted(shape) {
            // copy back data
            // find the shape index
            const idx = this.shapes
                .map((shape, index) => {
                    if (shape.name === shape.name) {
                        return index;
                    }
                })
                .filter((item) => item !== undefined);
            this.$emit('sidebar-entry-save', shape.name);
        },
        selectRow(row) {
            this.$refs.myTable.setCurrentRow(row);
        },
        handleSaveRow(index) {
            this.submitted(this.formData[index]);
            this.formData[index].edited = false;
        },
        handleClick(index) {
            this.formData[index].edited = true;
        }
    },
    watch: {
        selectedShapeName: function (newShape, oldShape) {
            // find index of new shape
            const idx = this.shapes
                .map((shape, index) => {
                    if (shape.name === newShape) {
                        return index;
                    }
                })
                .filter((item) => item !== undefined);
            this.selectRow(this.formData[idx]);
        },
        shapes() {
            this.formData = this.shapes;
        }
    }
};
</script>

<template>
    <div class="table-container">
        <el-table ref="myTable" :data="formData" style="width: 100%" :row-key="selectedShapeName" border @cell-mouse-enter="handleMouseEnter" @cell-mouse-leave="handleMouseLeave" highlight-current-row>
            <!-- Index Column -->
            <el-table-column prop="annotation.title" :label="buttonTitle" :min-width="20">
                <template v-slot="scope">
                    <span v-if="!justShow" class="font-bold">{{ scope.$index + 1 }}</span>
                    <span v-else>{{ scope.row.rectangleType }}.{{ scope.$index + 1 }}</span>
                </template>
            </el-table-column>

            <!-- Annotation Title Column -->
            <el-table-column v-if="hasTitle" prop="annotation.title" :label="titleColumnName" :min-width="20">
                <template v-slot="scope">
                    <span>{{ scope.row.annotation.title }}</span>
                </template>
            </el-table-column>

            <!-- Form Column -->
            <el-table-column :label="buttonText" :min-width="45" v-if="rectangleType != 'mask'">
                <template v-slot="scope">
                    <!--  模板編輯 -->
                    <el-input v-if="editMode && rectangleType != 'mask'" :class="{ 'disabled-input': !scope.row.edited }" v-model="scope.row.annotation.title" @click="handleClick(scope.$index)">{{ scope.row.annotation.title }}</el-input>
                    <!--  模板編輯確認 -->
                    <el-input v-else-if="!editMode && justShow" v-model="scope.row.annotation.title" disabled>{{ scope.row.annotation.title }}</el-input>
                    <!--  辨認結果 -->
                    <el-input v-else-if="scope.row.annotation.text != undefined" :class="{ 'disabled-input': !scope.row.edited }" v-model="scope.row.annotation.text" @click="handleClick(scope.$index)">{{ scope.row.annotation.text }}</el-input>
                </template>
            </el-table-column>

            <!-- Save Button Column -->
            <el-table-column v-if="showSaveButton" label="" :min-width="20">
                <template v-slot="scope">
                    <el-button type="default" @click="handleSaveRow(scope.$index)">確認</el-button>
                </template>
            </el-table-column>

            <!-- Delete Shape Column -->
            <el-table-column v-if="editMode" label="" :min-width="20">
                <template v-slot="scope">
                    <a href="#" @click.prevent="deleteShape(scope.row)" title="Delete">
                        <icon type="delete-shape" fill="red" />
                    </a>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>
<style scoped>
.disabled-input {
    opacity: 0.5;
}
.table-container {
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin: 2px;
    margin-bottom: 5px;
}
</style>
