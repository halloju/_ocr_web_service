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
            buttonTitle: this.justShow ? '區塊類型' : 'index'
            // shouldBeDisabled: false
        };
    },
    created() {
        console.log(this.shapes);
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
        inputClass(row) {
            return {
                'disabled-input': !row.edited
            };
        },
        inputValue(row) {
            if (this.editMode || this.justShow) {
                return row.annotation.title;
            } else if (row.annotation.text !== undefined) {
                return row.annotation.text;
            }
            return '';
        },
        handleInput(event, row) {
            if (this.editMode || this.justShow) {
                row.annotation.title = event.target.value;
            } else if (row.annotation.text !== undefined) {
                row.annotation.text = event.target.value;
            }
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
            <!-- Annotation Title Column -->
            <el-table-column prop="annotation.title" :label="buttonTitle" :min-width="20">
                <template v-slot="scope">
                    <span v-if="!justShow" class="font-bold">{{ scope.$index }}.</span>
                    <span v-else>{{ scope.row.rectangleType }}.{{ scope.$index }}</span>
                </template>
            </el-table-column>

            <!-- Form Column -->
            <el-table-column v-if="showFormColumn" :label="buttonText" :min-width="50">
                <template v-slot="scope">
                    <el-input :class="inputClass(scope.row)" :value="inputValue(scope.row)" @input="handleInput($event, scope.row)" @click="handleClick(scope.$index)">
                        {{ inputValue(scope.row) }}
                    </el-input>
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
