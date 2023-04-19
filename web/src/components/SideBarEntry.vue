<script>
import Nl2br from 'vue3-nl2br';
import Icon from '@/components/Icon.vue';

export default {
    components: {
        Icon,
        Nl2br
    },
    props: ['shape', 'editMode', 'selectedShapeName', 'currentHoverShape', 'justShow', 'rectangleType'],
    data() {
        return {
            annotation_title: '要項名稱：',
            annotation_text: '要項內容：',
            submit: '確認',
            active: false,
            // form data as copy
            formData: {
                title: '',
                text: '',
                linkTitle: '',
                link: ''
            }
        };
    },
    created() {
        console.log(this.rectangleType);
        if (this.shape) {
            this.formData.title = this.shape.annotation.title;
            this.formData.text = this.shape.annotation.text;
            this.formData.linkTitle = this.shape.annotation.linkTitle;
            this.formData.link = this.shape.annotation.link;
        }
    },
    methods: {
        handleMouseEnter() {
            this.$emit('sidebar-entry-enter', this.shape.name);
        },
        handleMouseLeave() {
            this.$emit('sidebar-entry-leave', this.shape.name);
        },
        toggleContent() {
            // slide up/down
            this.$refs.panel.style.maxHeight = this.active ? null : this.$refs.panel.scrollHeight + 'px';
            // activation
            this.active = !this.active;
        },
        deleteShape() {
            this.$emit('sidebar-entry-delete', this.shape.name);
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
        }
    },
    watch: {
        selectedShapeName: function (newShape, oldShape) {
            if (newShape === this.shape.name) {
            }
            if (!this.active && newShape === this.shape.name) {
                this.toggleContent();
            } else if (this.active && newShape !== this.shape.name) {
                this.toggleContent();
            }
        },
        shape() {
            this.formData.title = this.shape.annotation.title;
            this.formData.text = this.shape.annotation.text;
            this.formData.linkTitle = this.shape.annotation.linkTitle;
            this.formData.link = this.shape.annotation.link;
        }
    }
};
</script>

<template>
    <div class="pa-side-bar-entry" @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave" :class="{ 'is-selected-target': selectedShapeName === shape.name, 'is-hover-target': currentHoverShape === shape.name }">
        <button type="button" @click.prevent.stop="toggleContent" class="pa-accordion" :class="{ 'is-active': active }">
            <!-- <icon :type="shape.type" /> -->
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
                    <input type="text" name="title" :id="shape.name + '-title'" v-model="formData.title" />
                    <button  type="submit">{{ submit }}</button>
                </form>
            </template>
            <template v-else>
                <form  v-if="formData.text != undefined && formData.text != ''" class="pa-annotation-form" @submit.prevent.stop="submitted">
                    <label :for="shape.name + '-text'">{{ annotation_text }}</label>
                    <textarea  name="text" :id="shape.name + '-text'" v-model="formData.text" :disabled="justShow" readonly />
                </form>
            </template>
        </div>
    </div>
</template>
