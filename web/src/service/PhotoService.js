const contextPath = import.meta.env.BASE_URL;

export function usePhotoService() {
    function getImages() {
        return fetch(contextPath + 'demo/data/photos.json')
            .then((res) => res.json())
            .then((d) => d.data);
    }

    return { getImages };
}
