<script>
import Nl2br from 'vue3-nl2br';
import Icon from '@/components/Icon.vue';

export default {
    components: {
        Icon,
        Nl2br
    },
    props: ['shapes', 'editMode', 'selectedShapeName', 'currentHoverShape', 'justShow', 'rectangleType', 'delete_shape'],
    data() {
        return {
            annotation_title: '要項名稱：',
            annotation_text: '要項內容：',
            submit: '確認',
            active: false,
            // form data as copy
            formData: [],
            // shouldBeDisabled: false
        };
    },
    created() {
        if (this.shapes) {
            this.formData = this.shapes
            
            // this.formData.title = this.shape.annotation.title;
            // this.formData.text = this.shape.annotation.text;
            // this.formData.linkTitle = this.shape.annotation.linkTitle;
            // this.formData.link = this.shape.annotation.link;
        }
    },
    methods: {
        handleMouseEnter(shape) {
            this.$emit('sidebar-entry-enter', shape.name);
        },
        handleMouseLeave(shape) {
            this.$emit('sidebar-entry-leave', shape.name);
        },
        toggleContent() {
            // slide up/down
            this.$refs.panel.style.maxHeight = this.active ? null : this.$refs.panel.scrollHeight + 'px';
            // activation
            this.active = !this.active;
        },
        deleteShape(shape) {
            this.$emit('sidebar-entry-delete', shape.name);
        },
        submitted() {
            // copy back data
            this.shape.annotation.title = this.formData.title;
            this.shape.annotation.text = this.formData.text;
            this.shape.annotation.linkTitle = this.formData.linkTitle;
            this.shape.annotation.link = this.formData.link;

            // close entry
            this.toggleContent();
            this.$emit('sidebar-entry-save', this.shape.name);
        },
        truncateText(text, maxLength) {
            if (text.length > maxLength) {
                return text.substring(0, maxLength) + '...';
            }
            return text;
        },
        selectRow(row) {
            this.$refs.myTable.setCurrentRow(row);
        }
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
            // this.formData.title = this.shape.annotation.title;
            // this.formData.text = this.shape.annotation.text;
            // this.formData.linkTitle = this.shape.annotation.linkTitle;
            // this.formData.link = this.shape.annotation.link;
        }
    }
};
</script>

<template>
    <div>
        <div class="flex align-items-center justify-content-center font-bold m-2 mb-5">
            <el-table ref='myTable' :data="formData" style="width: 100%" :row-key="selectedShapeName" border @cell-mouse-enter="handleMouseEnter" @cell-mouse-leave="handleMouseLeave" highlight-current-row>
                
                <!-- Annotation Title Column -->
                <el-table-column prop="annotation.title" label="區塊" sortable :min-width="30">
                    <template v-slot="scope">
                        <span v-if="scope.row.annotation.title" class="font-bold">{{ scope.row.annotation.title }}.</span>
                    </template>
                </el-table-column>
                
                <!-- Form Column -->
                <el-table-column label="欄位" :min-width="50">
                    <template v-slot="scope">
                        <form v-if="editMode && rectangleType != 'mask'" @submit.prevent.stop="formSubmitted(scope.row)">
                            <input type="text" name="title" :id="scope.row.name + '-title'" required v-model="scope.row.annotation.title" />
                        </form>
                        <form v-else-if="scope.row.annotation.text != undefined" @submit.prevent.stop="formSubmitted(scope.row)">
                            <textarea name="text" :id="scope.row.name + '-text'" v-model="scope.row.annotation.text"></textarea>
                        </form>
                    </template>
                </el-table-column>
                

                <el-table-column label="Actions" :min-width="20">
                    <template v-slot="scope">
                        <span v-if="editMode">
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


    <!-- <div class="pa-side-bar-entry" @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave" :class="{ 'is-selected-target': selectedShapeName === shape.name, 'is-hover-target': currentHoverShape === shape.name }">
        <button type="button" @click.prevent.stop="toggleContent" class="pa-accordion" :class="{ 'is-active': active }">
            <span v-if="shape.annotation.title" class="pa-side-bar-title" style="font-weight:bold;">{{ shape.annotation.title }}.</span>
            <span v-if="editMode && (active || selectedShapeName === shape.name)" class="pa-side-bar-icons">
                <a href="#" @click.prevent="deleteShape" :title="delete_shape"><icon type="delete-shape" fill="red" /></a>
            </span>
            {{ truncateText(formData.text, 10) }}
        </button>
        <div class="pa-panel" ref="panel">
            <template v-if="editMode">
                <form class="pa-annotation-form" v-if="rectangleType != 'mask'"  @submit.prevent.stop="submitted">
                    <label :for="shape.name + '-title'">{{ annotation_title }}</label>
                    <input type="text" name="title" :id="shape.name + '-title'"  required v-model="formData.title" />
                    <button  type="submit">{{ submit }}</button>
                </form>
            </template>
            <template v-else>
                <form  v-if="formData.text != undefined" class="pa-annotation-form" @submit.prevent.stop="submitted">
                    <label v-if="!justShow" :for="shape.name + '-text'">{{ annotation_text }}</label>
                    <textarea v-if="!justShow" name="text" :id="shape.name + '-text'" v-model="formData.text" />
                    <button v-if="!justShow" type="submit">{{ submit }}</button>
                </form>
            </template>
        </div>
    </div> -->
</template>
