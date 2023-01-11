<script scope>
export default {
    name: 'Rect',
    components: {},
    computed: {
        recs() {
            return this.$store.state[this.boxName];
        }
    },
    methods: {
        handleTransformEnd(e) {
            // shape is transformed, let us save new attrs back to the node
            // find element in our state
            const rect = this.recs.find((r) => r.name === e.target.attrs.name);
            // const transformer = e.target.getTransform();
            // const next = transformer.point({ x: 0, y: 0 });

            rect.startPointX = e.target.x();
            rect.startPointY = e.target.y();
            rect.scaleX = e.target.attrs.scaleX;
            rect.scaleY = e.target.attrs.scaleY;
            rect.endPointX = e.target.x() + rect.width * rect.scaleX;
            rect.endPointY = e.target.y() + rect.height * rect.scaleY;
        },
        handleDragEnd(e) {
            e.cancelBubble = true;
            const rect = this.recs.find((r) => r.name === e.target.attrs.name);
            const pos = e.target.getPosition();
            // update the state
            rect.startPointX = pos.x;
            rect.startPointY = pos.y;
            rect.endPointX = pos.x + rect.width * rect.scaleX;
            rect.endPointY = pos.y + rect.height * rect.scaleY;
        },
        handleDragBond(e) {
            const rect = this.recs.find((r) => r.name === e.target.attrs.name);
            const pos = e.target.getPosition();

            if (pos.x < 0) {
                e.target.x(0);
            }
            if (pos.y < 0) {
                e.target.y(0);
            }
            if ((pos.x + rect.width * rect.scaleX) > this.imageAttrs.width) {
                e.target.x(this.imageAttrs.width - rect.width * rect.scaleX);
            }
            if ((pos.y + rect.height * rect.scaleY) > this.imageAttrs.height) {
                e.target.y(this.imageAttrs.height - rect.height * rect.scaleY);
            }
        }
    },
    props: {
        boxName: {
            type: String,
            required: true
        },
        fillColor: {
            type: Object,
            default() {
                return {
                    r: 0,
                    g: 0,
                    b: 0,
                    a: 0.3
                };
            }
        },
        imageAttrs: {
            type: Object,
            default() {
                return {
                    width: 0,
                    height: 0
                };
            }
        }
    }
};
</script>

<template>
    <v-rect
        v-for="(rec, index) in recs"
        :key="index"
        :name="rec.name"
        :config="{
            width: Math.abs(rec.width),
            height: Math.abs(rec.height),
            fill: `rgb(${this.fillColor.r},${this.fillColor.g},${this.fillColor.b},${this.fillColor.a})`,
            stroke: 'rgb(20,20,200,1)',
            strokeWidth: 0.5,
            x: Math.min(rec.startPointX, rec.startPointX + rec.width),
            y: Math.min(rec.startPointY, rec.startPointY + rec.height)
        }"
        @transformend="handleTransformEnd"
        @dragend="handleDragEnd"
        @dragmove="handleDragBond"
    >
    </v-rect>
    <v-text v-for="(rec, index) in recs" :config="{ text: `No.` + index + `\n要項名稱：` + rec.name, fontSize: 13, x: Math.min(rec.startPointX, rec.startPointX + rec.width), y: Math.min(rec.startPointY, rec.startPointY + rec.height) }" />
</template>
