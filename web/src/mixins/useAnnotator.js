import { ref } from 'vue';

export default function useAnnotator() {
    // const rectangleTypes = ref(['text', 'box', 'mask']);
    const rectangleTypes = ref([
        { name: '文字', code: 'text' },
        { name: '方塊', code: 'box' },
        { name: '遮罩', code: 'mask' }
    ]);

    const generatePointsList = (points) => {
        if (points === undefined || points.length === 0) {
            return {
                label_x: 0,
                label_y: 0,
                label_width: 0,
                label_height: 0
            };
        }
        // find the min and max x and y
        let minX = Math.min(...points.map((point) => point[0]));
        let maxX = Math.max(...points.map((point) => point[0]));
        let minY = Math.min(...points.map((point) => point[1]));
        let maxY = Math.max(...points.map((point) => point[1]));

        return {
            label_x: minX,
            label_y: minY,
            label_width: maxX - minX,
            label_height: maxY - minY
        };
    };

    const getFillColorByRectangleType = (rectangleType) => {
        switch (rectangleType) {
            case 'text':
                return '#b0c4de'; // blue color for text box
            case 'box':
                return '#7eff70'; // Green color for box
            case 'mask':
                return '#d1a46a'; // Brown color for mask box
            default:
                return '#b0c4de'; // Default color for other types
        }
    };

    const createShape = (fill, element, index) => {
        const myContent = element.hasOwnProperty('tag') ? element['tag'] : '';
        const { label_x, label_y, label_width, label_height } = generatePointsList(element.points);

        return {
            type: 'rect',
            name: 'shape_' + index,
            fill: fill,
            opacity: 0.5,
            stroke: '#0000ff',
            draggable: true,
            strokeWidth: 2,
            strokeScaleEnabled: false,
            annotation: {
                title: myContent,
                text: '',
                linkTitle: '',
                link: ''
            },
            x: label_x,
            y: label_y,
            width: label_width,
            height: label_height,
            scaleX: 1,
            scaleY: 1,
            rectangleType: element.type || 'text'
        };
    };

    const generateShapeList = (rectangleType, boxes) => {
        // Create shapes(list) from the data according to the element type
        let fill = getFillColorByRectangleType(rectangleType);
        const shapeList = boxes.map((element, index) => createShape(fill, element, index));
        return shapeList;
    };

    const saveShapeList = (rectangleType, shapeList) => {
        // Save the shape list to the local storage
        localStorage.setItem(rectangleType, shapeList);
    };

    const loadShapeList = (rectangleType) => {
        // Load the shape list from the local storage
        return localStorage.getItem(rectangleType);
    };

    const parseTemplateDetail = (res, rectangleType) => {
        // Parse the template details to get the boxes
        let boxes = res.points_list.filter((item) => item.type === rectangleType);
        return generateShapeList(rectangleType, boxes);
    };

    const parseOcrDetail = (res) => {
        // Parse the ocr details to get the boxes
        let shapes = [];
        res.data_results.forEach(function (element, index) {
            var { label_x, label_y, label_width, label_height } = generatePointsList(element.points);
            let title = element.hasOwnProperty('tag') ? element['tag'] : '';
            shapes.push({
                type: 'rect',
                name: 'shape_' + index,
                fill: '#b0c4de',
                opacity: 0.5,
                stroke: '#0000ff',
                draggable: true,
                strokeWidth: 2,
                strokeScaleEnabled: false,
                annotation: {
                    title: title,
                    text: element.text,
                    linkTitle: '',
                    link: ''
                },
                x: label_x,
                y: label_y,
                width: label_width,
                height: label_height,
                rectangleType: 'text'
            });
        });
        return shapes;
    };

    return {
        rectangleTypes,
        generatePointsList,
        getFillColorByRectangleType,
        createShape,
        generateShapeList,
        parseTemplateDetail,
        saveShapeList,
        loadShapeList,
        parseOcrDetail
    };
}
