ymaps.ready(init);
let formMap = null;

function loadMemoriesDataFromServer() {
    /**
     * Подгружает и рендерит точки на карту
     */
    function addPlaceMarkMemoriToMap(coords, memories_id, imageHrf = null) {
        /**
         * Добавляет на карту балун с картинкой ( если есть ) или обычный
         * указатель в противном случае. Создает обработчик, чтобы при нажатии
         * на хинт лента листалась к воспоминанию
         * coords - массив из 2 координат
         * memories_id - id воспоминания. Без #
         * imageHrf - ссылка на картинку /media/img/...
         */
        let balun = null;
        if (imageHrf) {
            const imageLayer = {
                iconLayout: 'default#imageWithContent',
                iconImageOffset: [-25, -50],
                iconContentLayout: ymaps.templateLayoutFactory.createClass(
                    '<div style="width: 40px; border: #0f0f0f 2px solid; overflow: hidden; height: 60px; ' +
                    'background-image: url(' + imageHrf + '); background-size: cover; ' +
                    'background-repeat: no-repeat;' +
                    'background-position: center; border-radius: 5px 0 5px 0;"></div>'
                )
            }
            balun = new ymaps.Placemark(coords, {
                hintContent: 'Кликните, чтобы перейти к воспоминанию '
            }, imageLayer)
        } else {
            balun = new ymaps.Placemark(coords, {
                hintContent: 'Кликните, чтобы перейти к воспоминанию '
            })
        }


        balun.events.add('click', () => {
            /**
             * Обработчик, который лестает ленту и запрещает листать экран
             */
            if (window.location.hash.slice(1) === memories_id) {
                const currentScrollY = window.scrollY;
                window.location.hash = 'firs-el'
                window.scrollTo({
                    top: currentScrollY,
                });
            } else {
                const currentScrollY = window.scrollY;
                window.location.hash = memories_id
                window.scrollTo({
                    top: currentScrollY,
                });
            }
        })

        formMap.geoObjects.add(balun);
    }

    const dataUrl = 'https://sabaton-enjoyer.online/map/get-place-marks-data-list/'
    fetch(dataUrl)
        .then(response => response.json())
        .then(jsonData => {
            jsonData.forEach((item) => {
                const coords = [item.coord1, item.coord2]
                const memories_id = 'memories_' + item.id
                addPlaceMarkMemoriToMap(coords, memories_id, item.image)
            })
        })

}

function init() {
    formMap = new ymaps.Map("mapWithPlaces", {
        center: [55.76, 37.64],
        zoom: 5
    });

    formMap.controls.add('zoomControl');
    formMap.controls.add('typeSelector');
    formMap.controls.add('searchControl');

    loadMemoriesDataFromServer()
}


