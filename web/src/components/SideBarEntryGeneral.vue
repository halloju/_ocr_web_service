<script>
import ViewEditResultColumn from '@/components/CustomizeColumns/ViewEditResultColumn.vue';
import EditModeColumn from '@/components/CustomizeColumns/EditModeColumn.vue';
import ViewRecognitionResultColumn from '@/components/CustomizeColumns/ViewRecognitionResultColumn.vue';
import BrowseModeComponent from '@/components/CustomizeColumns/BrowseModeComponent.vue';

export default {
    components: {
        ViewEditResultColumn,
        ViewRecognitionResultColumn,
        EditModeColumn,
        BrowseModeComponent
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
        },
        tableHeight: {
            type: String,
            default: '375'
        }
    },
    data() {
        return {
            submit: '確認',
            // form data as copy
            formData: [],
            buttonText: this.editMode ? '欄位命名' : '欄位',
            buttonTitle: this.justShow ? '區塊類型' : 'index',
            filterButtonText: '區塊包含的字符',
            titleColumnName: '欄位名稱',
            resultColumnName: '辨識結果',
            checkColumnName: '確認',
            deleteColumnName: '刪除',
            NameDict: {
                tchinese: '繁體中文',
                english: '英文',
                number: '數字',
                symbol: '符號',
                space: '空白',
                taiwan_id: '台灣身份證字號',
                currency_code: '幣別代碼',
                date: '日期',
                sealbox: '原留印鑑框',
                checkbox: '勾選框'
            },
            activeTab: 'first'
        };
    },
    created() {
        if (this.shapes) {
            this.formData = this.shapes;
        }
        console.log('side-bar created:', this.formData);
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
        tableRowClassName({ row, rowIndex }) {
            if (!this.editMode) return;
            if ('isComplete' in row && !row.isComplete) return 'warning-row';
            else return null;
        },
        updateCompleteStatus(rowIndex, completeStatus) {
            this.formData[rowIndex].isComplete = completeStatus;
        },
        handleMouseEnter(shape) {
            this.$emit('sidebar-entry-enter', shape.name);
        },
        handleMouseLeave(shape) {
            this.$emit('sidebar-entry-leave', shape.name);
        },
        handleDeleteShape(shape) {
            this.$emit('sidebar-entry-delete', shape.name);
        },
        submitted(shape) {
            console.log('submitted:', shape);
            this.$emit('sidebar-entry-save', shape);
        },
        selectRow(row) {
            this.$refs.myTable.setCurrentRow(row);
        },
        handleSaveRow(rowIndex, updatedText) {
            const updatedAnnotation = { ...this.formData[rowIndex].annotation, text: updatedText };
            const updatedItem = { ...this.formData[rowIndex], annotation: updatedAnnotation };
            this.formData = [...this.formData.slice(0, rowIndex), updatedItem, ...this.formData.slice(rowIndex + 1)];
            this.submitted(this.formData[rowIndex]);
            this.formData[rowIndex].edited = false;
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
        <el-tabs type="border-card" class="tabs-container" v-model="activeTab">
            <el-tab-pane label="編輯" name="first">
                <el-table
                    ref="myTable"
                    :data="formData"
                    style="width: 100%"
                    :row-class-name="tableRowClassName"
                    :row-key="selectedShapeName"
                    border
                    @cell-mouse-enter="handleMouseEnter"
                    @cell-mouse-leave="handleMouseLeave"
                    highlight-current-row
                    :max-height="tableHeight"
                >
                    <!-- Index Column -->
                    <el-table-column prop="annotation.title" :label="buttonTitle" :min-width="20">
                        <template v-slot="scope">
                            <span class="font-bold">{{ scope.$index + 1 }}</span>
                        </template>
                    </el-table-column>

                    <!-- View Recognition Result Components -->
                    <view-recognition-result-column @save="handleSaveRow" @click="handleClick" :buttonText="resultColumnName" :checkColumnName="checkColumnName"> </view-recognition-result-column>
                    <!-- View Recognition Result Components -->
                </el-table>
            </el-tab-pane>
            <el-tab-pane label="瀏覽" name="second">
                <browse-mode-component :formData="formData"></browse-mode-component>
            </el-tab-pane>
        </el-tabs>
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
/* Add this CSS to make your tabs full width */
.el-tabs__header {
    display: flex;
    justify-content: space-around; /* This will distribute the tabs evenly */
}

/* If your tabs are wrapped inside another container, you might need to make sure that this container is full width as well */
.tabs-container {
    width: 100%; /* Assuming your table is also full width of its container */
}

.tabs-container .el-tabs__header {
    display: flex;
    justify-content: space-around;
}

.table-container {
    width: 100%; /* Ensure the table container is also full width */
}
</style>