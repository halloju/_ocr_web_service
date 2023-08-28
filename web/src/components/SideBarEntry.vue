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
        }
    },
    data() {
        return {
            annotation_title: '要項名稱：',
            annotation_text: '要項內容：',
            submit: '確認',
            active: false,
            // form data as copy
            formData: [],
            buttonText: this.editMode ? '欄位命名' : '欄位',
            buttonTitle: this.justShow ? '區塊類型' : 'index',
            // shouldBeDisabled: false
        };
    },
    created() {
        console.log(this.shapes);
        if (this.shapes) {
            this.formData = this.shapes
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
            const idx = this.shapes.map((shape, index) => {
                if (shape.name === shape.name) {
                    return index;
                }
            }).filter(item => item !== undefined);
            this.$emit('sidebar-entry-save', shape.name);
        },
        truncateText(text, maxLength) {
            if (text.length > maxLength) {
                return text.substring(0, maxLength) + '...';
            }
            return text;
        },
        selectRow(row) {
            this.$refs.myTable.setCurrentRow(row);
        },
        toggleEditSave(index) {
            this.formData[index].edited = !this.formData[index].edited;
            this.buttonText[index] = this.formData[index].edited ? 'Save' : 'Edit';
        },
        handleSaveRow(index) {
            this.submitted(this.formData[index]);
            this.formData[index].edited = false;
        },
        handleClick(index) {
            console.log(index);
            this.formData[index].edited = true;
        },
    },
    watch: {
        selectedShapeName: function (newShape, oldShape) {
            // find index of new shape
            const idx = this.shapes.map((shape, index) => {
                if (shape.name === newShape) {
                    return index;
                }
            }).filter(item => item !== undefined);
            this.selectRow(this.formData[idx])
        },
        shapes() {
            this.formData = this.shapes
        }
    }
};
</script>

<template>
    <div>
        <div class="flex align-items-center justify-content-center font-bold m-2 mb-5">
            <el-table ref='myTable' :data="formData" style="width: 100%" :row-key="selectedShapeName" border @cell-mouse-enter="handleMouseEnter" @cell-mouse-leave="handleMouseLeave" highlight-current-row>
                
                <!-- Annotation Title Column -->
                <el-table-column prop="annotation.title" :label="buttonTitle" :min-width="20">
                    <template v-slot="scope">
                        <span v-if="!justShow" class="font-bold">{{ scope.$index }}.</span>
                        <span v-else>{{ scope.row.rectangleType }}.</span>
                    </template>
                </el-table-column>
                
                <!-- Form Column -->
                <el-table-column :label="buttonText" :min-width="50">
                    <template v-slot="scope">
                        <!--  模板編輯 -->
                        <el-input v-if="editMode && rectangleType != 'mask'" :class="{ 'disabled-input': !scope.row.edited }" v-model="scope.row.annotation.title" @click="handleClick(scope.$index)" >{{ scope.row.annotation.title }}</el-input>
                        <!--  模板編輯確認 -->
                        <el-input v-else-if="!editMode && justShow" v-model="scope.row.annotation.title" disabled >{{ scope.row.annotation.title }}</el-input>
                        <!--  辨認結果 -->
                        <el-input v-else-if="scope.row.annotation.text != undefined" :class="{ 'disabled-input': !scope.row.edited }" v-model="scope.row.annotation.text" @click="handleClick(scope.$index)" >{{ scope.row.annotation.text }}</el-input>
                    </template>
                </el-table-column>

                <el-table-column label="" :min-width="20" v-if="editMode || !justShow">
                    <template v-slot="scope">
                        <span >
                            <el-button type="default" @click="handleSaveRow(scope.$index)">確認</el-button>
                        </span>
                    </template>
                </el-table-column>

                <el-table-column label="" :min-width="20" v-if="editMode">
                    <template v-slot="scope">
                        <span >
                            <a href="#" 
                            @click.prevent="deleteShape(scope.row)" 
                            title="Delete">
                                <icon type="delete-shape" fill="red" />
                            </a>
                        </span>
                    </template>
                </el-table-column>

            </el-table>
        </div>
    </div>
</template>
<style scoped>
.disabled-input {
    opacity: 0.5;
}
</style>