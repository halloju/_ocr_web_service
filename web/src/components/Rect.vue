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
            const rect = this.recs.find((r) => r.name === e.target.attrs.name);
            const pos = e.target.getPosition();
            // update the state
            rect.startPointX = pos.x;
            rect.startPointY = pos.y;
            rect.endPointX = pos.x + rect.width * rect.scaleX;
            rect.endPointY = pos.y + rect.height * rect.scaleY;
        },
        handleMouseMove(e) {
            const rect = this.recs.find((r) => r.name === e.target.attrs.name);
            var mousePos = e.target.getStage().getPointerPosition();
            var tooltip = e.target.getStage().findOne('.tooltip');
            tooltip.position({
                x: mousePos.x,
                y: mousePos.y
            });
            tooltip.text(rect.name);
            tooltip.show();
        },
        handleMouseOut(e) {
            var tooltip = e.target.getStage().findOne('.tooltip');
            tooltip.hide();
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
        draggable="true"
        @transformend="handleTransformEnd"
        @dragend="handleDragEnd"
        @mouseover="handleMouseMove"
        @mouseout="handleMouseOut"
    />
</template>
