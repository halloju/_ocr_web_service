<script>
import Icon from '@/components/Icon.vue';
import Loader from '@/components/Loader.vue';
import SideBarEntry from '@/components/SideBarEntry.vue';
import useAnnotator from '@/mixins/useAnnotator.js';
export default {
    components: {
        SideBarEntry,
        Icon,
        Loader
    },
    props: {
        containerId: String,
        imageSrc: String,
        dataCallback: Function,
        localStorageKey: String,
        width: String,
        height: String,
        editMode: Boolean,
        initialData: Object,
        image_cv_id: String,
        justShow: Boolean,
        rectangleType: String,
        isVertical: Boolean,
        setShowText: {
            type: Boolean,
            default: false
        }},
    data() {
        return {
            image: null,
            stageSize: {
                width: null,
                height: null
            },
            scale: 1, // current scale
            shapes: [], // shape container
            selectedShapeName: '', // currently selected shape
            currentHoverShape: '', // hovering over certain shape
            isLoading: true, // loading image?
            isShapesVisible: true, // show shapes?
            isAddingPolygon: false, // currently in polygon add mode?
            polygonPoints: [],
            polygonAddShapes: [],
            callback: undefined, // actual callback function
            formData: {
                title: '',
                text: '',
                linkTitle: '',
                link: ''
            },
            isShowText: this.setShowText,
            isTitle: true
        };
    },
    watch: {
        imageSrc() {
            this.loadImage();
        },
        initialData() {
            this.load();
        }
    },
    computed: {
        polygonPointsConfig() {
            return {
                points: this.polygonPoints,
                ...this.getBaseShapeForPolygon(),
                closed: true
            };
        }
    },
    // created live cycle hook
    created() {
        // set defaults
        if (this.isVertical) {
            this.containerClass = 'pa-containerVert'
            this.infoBarClass = 'pa-infobarVert'
        } else{
            this.containerClass = 'pa-container'
            this.infoBarClass = 'pa-infobar'
        }
        // load image
        this.loadImage();
    },
    mounted() {
        this.stageSize.width = this.$refs.main.clientWidth; // - 2 for border
        this.stageSize.height = this.$refs.main.clientHeight;
        if (!this.stageSize.width || isNaN(this.stageSize.width)) this.stageSize.width = parseInt(this.width)-parseInt("4rem");
        if (!this.stageSize.height || isNaN(this.stageSize.height)) this.stageSize.height = parseInt(this.height)*0.6;
        document.addEventListener('keydown', this.handleKeyEvent);
        // try to load from local storage or local data
        this.load();
    },
    beforeUnmount() {
        document.removeEventListener('keydown', this.handleKeyEvent);
    },
    setup() {
        // Use the useAnnotator function
        const { getFillColorByRectangleType, rectangleTypes } = useAnnotator();

        // Expose the methods to the template and Options API methods
        return {
            rectangleTypes,
            getFillColorByRectangleType
        };
    },
    methods: {
        getMiddlePosition() {
            const image = this.$refs.stage.getNode();
            const width = image.width();
            const height = image.height();
            const scaleX = image.scaleX();
            const scaleY = image.scaleY();
            const position = {x: width / (4 * scaleX) - image.x(), y: height / (2 * scaleY) - image.y()};
            return position;
        },
        loadImage() {
            // reset scale to 1
            this.scale = 1;
            const image = new window.Image();
            image.src = this.imageSrc;
            image.onload = () => {
                // set image only when it is loaded
                this.image = image;
                // adapt initial scale to fit canvas
                this.changeScale(-1 + Math.min(this.stageSize.width / image.width, this.stageSize.height / image.height));
                // loading finished
                this.isLoading = false;
            };
            // define callback function
            this.callback =
                this.dataCallback &&
                typeof eval(this.dataCallback) && // eslint-disable-line no-eval
                eval(this.dataCallback); // eslint-disable-line no-eval
        },
        // handle transformation of elements
        handleStageMouseDown(e) {
            // adding polygon shape?
            if (this.isAddingPolygon) {
                e.evt.preventDefault();
                e.evt.stopPropagation();
                e.evt.stopImmediatePropagation();
                // right mouse button deletes last point
                if (e.evt.button === 2) this.removePolygonPoint();
                else if (e.evt.detail === 1) this.addPolygonPoint(); // ignore double clicks
                return; // no further stuff
            }
            // only handle left mouse button
            if (e.evt && e.evt.button !== 0) return;
            // in edit mode?
            if (this.editMode) {
                // edit mode only
                // clicked on stage - clear selection
                if (e.target === e.target.getStage()) {
                    this.selectedShapeName = '';
                    this.updateTransformer();
                    return;
                }
                // clicked on transformer - do nothing
                const clickedOnTransformer = e.target.getParent().className === 'Transformer';
                if (clickedOnTransformer) {
                    return;
                }
            }
            // find clicked shape by its name
            const name = e.target.name();
            const shape = this.shapes.find((r) => r.name === name);
            if (shape) {
                this.selectedShapeName = name;
            } else {
                this.selectedShapeName = '';
            }
            if (this.editMode) {
                this.updateTransformer();
            }
        },
        updateTransformer() {
            if (!this.editMode) return; // edit mode only
            // here we need to manually attach or detach Transformer node
            const transformerNode = this.$refs.transformer.getStage();
            const stage = transformerNode.getStage();
            const { selectedShapeName } = this;
            const selectedNode = stage.findOne('.' + selectedShapeName);
            // do nothing if selected node is already attached
            if (selectedNode === transformerNode.node()) {
                return;
            }
            if (selectedNode) {
                // attach to another node
                transformerNode.attachTo(selectedNode);
            } else {
                // remove transformer
                transformerNode.detach();
            }
            transformerNode.getLayer().batchDraw();
        },
        cancelEvent(e) {
            e.evt.preventDefault();
        },
        addRectangle(rectangleType) {
            if (this.isAddingPolygon) return;
            const pos = this.getMiddlePosition();
            this.shapes.push({
                ...this.getBaseShape('rect', rectangleType),
                x: pos.x,
                y: pos.y,
                width: 200 / this.scale,
                height: 200 / this.scale
            });
            // call update
            this.shapesUpdated();
        },
        getBaseShape(type, rectangleType) {
            return {
                type: type,
                name: 'shape-' + new Date().valueOf(),
                fill: this.getFillColorByRectangleType(rectangleType),
                opacity: 0.5,
                stroke: '#0000ff',
                draggable: true,
                strokeWidth: 2,
                strokeScaleEnabled: false,
                scaleX: 1,
                scaleY: 1,
                annotation: {
                    title: null,
                    text: '',
                    linkTitle: '',
                    link: ''
                },
                rectangleType: rectangleType
            };
        },
        // delete shape
        deleteShape(name) {
            const idx = this.shapes.findIndex((r) => r.name === name);
            if (idx >= 0) {
                if (name === this.selectedShapeName) {
                    this.selectedShapeName = '';
                    this.updateTransformer();
                }
                this.shapes.splice(idx, 1);
                // call update
                this.shapesUpdated();
            }
        },
        // handle key events
        handleKeyEvent(event) {
            // shape selected?
            if (this.editMode && this.selectedShapeName) {
                // delete key pressed?
                if (event.key === 'Delete') this.deleteShape(this.selectedShapeName);
            }
            // TODO only if focued
            /* if (!this.selectedShapeName) {
                if (event.key === '+') this.changeScale(0.1);
            } */
        },
        // handle scaling of canvas
        handleScroll(e) {
            if (e.evt) {
                const event = e.evt;
                event.preventDefault();
                // Normalize wheel to +1 or -1.
                const wheel = event.deltaY < 0 ? 1 : -1;
                // calculate scale
                this.changeScale(wheel * 0.02);
            }
        },
        changeScale(diff) {
            let scale = this.scale + diff;
            // minimum and maximum
            if (scale < 0.1) scale = 0.1;
            if (scale > 5) scale = 5;
            // TODO: easing or timer - https://konvajs.org/docs/tweens/Common_Easings.html
            this.scale = scale;
        },
        // handle manipulation events
        handleDragEnd(event, shape) {
            shape.x = event.currentTarget.attrs.x;
            shape.y = event.currentTarget.attrs.y;
            // call update
            this.shapesUpdated();
        },
        handleTransform(event, shape) {
            shape.scaleX = event.currentTarget.attrs.scaleX;
            shape.scaleY = event.currentTarget.attrs.scaleY;
            shape.x = event.currentTarget.attrs.x;
            shape.y = event.currentTarget.attrs.y;
            // call update
            this.shapesUpdated();
        },
        // handle show stuff
        handleMouseEnter(name) {
            if (!this.isAddingPolygon) {
                this.$refs.stage.getStage().container().style.cursor = 'pointer';
                this.currentHoverShape = name;
            }
        },
        handleMouseLeave() {
            if (!this.isAddingPolygon) {
                this.$refs.stage.getStage().container().style.cursor = 'default';
                this.currentHoverShape = '';
            }
        },
        handleGlobalMouseEnter() {
            if (this.isAddingPolygon) this.$refs.stage.getStage().container().style.cursor = 'crosshair';
        },
        handleGlobalMouseLeave() {
            if (this.isAddingPolygon) this.$refs.stage.getStage().container().style.cursor = 'default';
        },
        handleSideBarMouseEnter(name) {
            if (!this.isAddingPolygon) {
                const idx = this.shapes.findIndex((r) => r.name === name);
                if (idx >= 0) {
                    this.shapes[idx].fill = '#ff4747';
                }
            }
        },
        handleSideBarMouseLeave(name) {
            if (!this.isAddingPolygon) {
                const idx = this.shapes.findIndex((r) => r.name === name);
                if (idx >= 0) {
                    this.shapes[idx].fill = this.getFillColorByRectangleType(this.shapes[idx].rectangleType);
                }
            }
        },
        formSubmitted(name) {
            // save correct color
            const idx = this.shapes.findIndex((r) => r.name === name);
            this.shapes[idx].fill = this.getFillColorByRectangleType(this.shapes[idx].rectangleType);
            // callback/persist
            this.shapesUpdated();
        },
        // toggle shapes shown or not
        toggleShowShapes() {
            // toggle
            this.$refs.items.getStage().canvas._canvas.style.opacity = this.isShapesVisible ? '0' : '1';
            // TODO: fade animation
            this.isShapesVisible = !this.isShapesVisible;
        },
        toggleShowTexts() {
            // toggle
            this.isShowText = !this.isShowText;
        },
        // callback on update
        shapesUpdated() {
            if (this.callback && typeof this.callback === 'function') {
                this.callback(this.shapes, this.image_cv_id);
            }
            // save to local storage, if defined
            if (this.localStorageKey) {
                sessionStorage.setItem(this.localStorageKey, JSON.stringify(this.shapes));
            }
        },
        load() {
            // load from initial data
            if (this.initialData) {
                this.shapes = this.initialData;
                if (this.shapes.length > 0) this.isTitle = this.shapes[0].annotation.title == '' ? false : true;
                // if we only show data, remove draggable from it
                if (!this.editMode) {
                    this.shapes.forEach((shape) => shape.draggable && delete shape.draggable);
                }
                return;
            }
            // load from local storage, if defined
            let data = [];
            if (this.localStorageKey === 'all') {
                const keys = ['text', 'box', 'mask'];
                for (let i = 0; i < keys.length; i++) {
                    const value = sessionStorage.getItem(keys[i]) || '[]';
                    data.push(...JSON.parse(value));
                }
            } else {
                const value = sessionStorage.getItem(this.localStorageKey) || '[]';
                data = JSON.parse(value);
            }
            this.shapes = data;
            // if we only show data, remove draggable from it
            if (!this.editMode) {
                this.shapes.forEach((shape) => shape.draggable && delete shape.draggable);
            }
        }
    }
};
</script>
<template>
    <div :id="containerId" :class="containerClass" :style="{ width: width + 'px', height: height + 'px' }">
        <div class="pa-canvas" :ref="'main'">
            <div class="pa-controls">
                <a href="#" @click.prevent="changeScale(0.1)" title="('zoom_in')"><icon type="zoom-in" /></a>
                <a href="#" @click.prevent="changeScale(-0.1)" title="('zoom_out')"><icon type="zoom-out" /></a>
                <hr />
                <a href="#" @click.prevent="toggleShowShapes" :title="isShapesVisible ? 'hide_shapes' : 'show_shapes'" v-if="!editMode"><icon :type="isShapesVisible ? 'shapes-off' : 'shapes-on'" /></a>
                <a href="#" @click.prevent="addRectangle(rectangleType)" title="add_rectangle'" v-if="editMode"><icon type="add-rectangle" :fill="isAddingPolygon ? 'gray' : 'currentColor'" /></a>
                <a href="#" v-if="this.isTitle" @click.prevent="toggleShowTexts" :title="isShowText ? 'show_texts' : 'hide_texts'"><icon :type="isShowText ? 'texts-off' : 'texts-on'" /></a>
            </div>
            <!-- TODO: Fix buttons above - unselect triggers before button can get selectedShapeName -->

            <v-stage
                :config="{
                    width: stageSize.width,
                    height: stageSize.height,
                    scaleX: scale,
                    scaleY: scale,
                    draggable: true
                }"
                @mousedown="handleStageMouseDown"
                @contextmenu="cancelEvent"
                @mouseenter="handleGlobalMouseEnter"
                @mouseleave="handleGlobalMouseLeave"
                @wheel="handleScroll"
                :ref="'stage'"
            >
                <v-layer ref="background">
                    <v-image
                        :config="{
                            image: image,
                            stroke: 'black'
                        }"
                    />
                </v-layer>
                <v-layer ref="items">
                    <template v-for="shape in shapes">
                        <v-rect
                            v-if="shape.type === 'rect'"
                            :config="shape"
                            :key="shape.name"
                            @dragend="handleDragEnd($event, shape)"
                            @transformend="handleTransform($event, shape)"
                            @mouseenter="handleMouseEnter(shape.name)"
                            @mouseleave="handleMouseLeave"
                        />
                        <v-text v-if="isShowText" :config="{ text: shape.annotation.title, fontSize: 30, x: Math.min(shape.x, shape.x + shape.width), y: Math.min(shape.y, shape.y + shape.height) }" />
                    </template>
                    <v-transformer ref="transformer" :rotateEnabled="false"  :keepRatio="false"  v-if="editMode" />
                </v-layer>
            </v-stage>

            <loader v-if="isLoading" />

            <div class="pa-polygon-hint" v-show="isAddingPolygon">polygon_help</div>
        </div>
        <div :class="infoBarClass">
            <side-bar-entry
                v-for="shape in shapes"
                :key="shape.name"
                :shape="shape"
                :edit-mode="editMode"
                :justShow="justShow"
                :selected-shape-name="selectedShapeName"
                :current-hover-shape="currentHoverShape"
                :rectangleType="rectangleType"
                v-on:sidebar-entry-enter="handleSideBarMouseEnter($event)"
                v-on:sidebar-entry-leave="handleSideBarMouseLeave($event)"
                v-on:sidebar-entry-delete="deleteShape($event)"
                v-on:sidebar-entry-save="formSubmitted($event)"
            />
        </div>
    </div>
</template>
<style lang="sass">
.pa-container
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif
  display: grid
  grid-template-columns: 2fr 1fr
  overflow: hidden
.pa-containerVert	
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif	
  display: grid	
  grid-template-rows: 6fr 4fr	
  overflow: hidden

.pa-canvas
  border: 1px solid #ccc
  position: relative
  overflow: hidden
.pa-controls
  position: absolute
  z-index: 100
  background-color: white
  padding: 0.3em
  left: 1em
  top: 1em
  border: 1px solid #333
  border-radius: 0.5em
  a
    color: #000
    display: block
    padding: 0.2em
  hr
    color: #000
    padding: 0
    margin: 0.1em 0 0.3em 0
.pa-polygon-hint
  position: absolute
  bottom: 1em
  left: 1em
  background-color: rgba(0, 0, 0, 0.6)
  color: #fff
  padding: 0.5em
  border-radius: 0.5em
  font-size: 90%
.pa-infobar
  margin-left: 5px
  overflow-y: scroll
.pa-infobarVert
  margin-top: 10px	
  overflow-y: scroll
// Loader component
.pa-loader
  position: absolute
  z-index: 102
  left: 0
  top: 0
  width: 100%
  height: 100%
  background-color: rgb(0,0,0)
  background-color: rgba(0,0,0,0.4)
// adapted from https://loading.io/css/
.lds-ring
  display: inline-block
  position: relative
  width: 100%
  height: 100%
.lds-ring div
  box-sizing: border-box
  display: block
  top: 30%
  left: calc(50% - 82px)
  position: absolute
  width: 164px
  height: 164px
  margin: 8px
  border: 18px solid #fff
  border-radius: 50%
  animation: lds-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite
  border-color: #fff transparent transparent transparent
.lds-ring div:nth-child(1)
  animation-delay: -0.45s
.lds-ring div:nth-child(2)
  animation-delay: -0.3s
.lds-ring div:nth-child(3)
  animation-delay: -0.15s
@keyframes lds-ring
  0%
    transform: rotate(0deg)
  100%
    transform: rotate(360deg)
// Side Bar Entry
.pa-side-bar-entry
  &.is-hover-target
    .pa-accordion
      background-color: #efc4b0
  &.is-selected-target
    .pa-accordion
      background-color: #efc4b0
.pa-accordion
  background-color: #eee
  color: #444
  cursor: pointer
  padding: 18px
  width: 100%
  text-align: left
  border: none
  outline: none
  transition: 0.4s
  margin-bottom: 2px
  &.is-active, &:hover
    background-color: #ccc
.pa-side-bar-title
  vertical-align: top
  padding-left: 5px
.pa-side-bar-icons
  float: right
.pa-annotation-text
  padding: 5px
.pa-panel
  padding: 0 18px
  background-color: white
  max-height: 0
  overflow: hidden
  transition: max-height 0.2s ease-out
.pa-annotation-link
  display: block
  text-align: center
  color: #000
  text-decoration: none
  background: lightgoldenrodyellow
  padding: 0.7em
  border: 0
  margin: 1em 0
  transition: background 0.5s ease-out
  &:hover, &:focus
    background: gold
.pa-annotation-form
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif
  display: grid
  grid-template-columns: auto 1fr
  grid-gap: 1em
  padding: 10px 0
  label
    grid-column: 1 / 2
    text-align: right
  button
    grid-column: 2 / 3
    background: lightgrey
    padding: 0.7em
    border: 0
    &:hover
      background: gold
  input, textarea
    grid-column: 2 / 3
    background: #fff
    border: 1px solid #9c9c9c
    &:focus
      outline: 3px solid gold
  textarea
    height: 10em
</style>
