function createPlaceMark(coords, coord1Node, coord2Node) {
    /**
     * создание балуна воспоминания на карте редактирования
     * @type {ymaps.Placemark}
     */
    const placeMark = new ymaps.Placemark(coords, {
        iconContent: 'Двигай меня',
    }, {
        balloonPanelMaxMapArea: 0,
        draggable: "true",
        preset: "islands#blueStretchyIcon",
    })

    placeMark.events.add('dragend', function (e) {
        let coords = placeMark.geometry.getCoordinates();
        movePlaceMarkAndRenderCoord(coords, placeMark, coord1Node, coord2Node)
    })
    return placeMark
}


function movePlaceMarkAndRenderCoord(coords, placeMark, coord1Node, coord2Node) {
    mapWithPlaces.panTo(coords, {duration: 500});
    placeMark.geometry.setCoordinates(coords);
    coord1Node.value = coords[0]
    coord2Node.value = coords[1]
}

function initMap(mapId, balunCoords, coord1Node, coord2Node) {
    /**
     * Инициализирует карту с балуном на месте воспоминания, который можно двигать
     * и сохранить в память новые воспоминания
     */
    ymaps.ready(() => {
        const editMap = new ymaps.Map(mapId, {
            center: [55.76, 37.64],
            zoom: 5
        });
        const placeMark = createPlaceMark(balunCoords, coord1Node, coord2Node)
        editMap.geoObjects.add(placeMark);

        editMap.events.add('click', function (e) {
            let coords = e.get('coords');
            movePlaceMarkAndRenderCoord(coords, placeMark, coord1Node, coord2Node)
        });
    });
}

function handleEditClick(e) {
    /**
     * при нажатии на кнопку редачить появляется карта, на которой можно поменять
     * местоположение метки и поменять все остальные поля (кроме картинки)
     */
    e.preventDefault()
    const parentForm = e.target.parentNode.parentNode
    const submitButton = parentForm.querySelector('.places-column__save-button')
    const coordsBlock = parentForm.querySelector('.places-column__coords-manager')
    const editMap = parentForm.querySelector('.memory-manager__map')
    const coord1Node = parentForm.querySelector('.places-column__coords1')
    const coord2Node = parentForm.querySelector('.places-column__coords2')
    const inputTitleNode = parentForm.querySelector('.places-column__tittle')

    // устанавливаем курсор в редактирование tittle и в конец
    inputTitleNode.focus()
    inputTitleNode.setSelectionRange(inputTitleNode.value.length, inputTitleNode.value.length);
    if (coordsBlock.style.display !== 'block') {
        // Если менюшка была закрыта
        coordsBlock.style.display = 'block'
        submitButton.style.display = 'block'
        let coords = [parseFloat(coord1Node.value), parseFloat(coord2Node.value)]
        initMap(editMap.id, coords, coord1Node, coord2Node)

        const inputTitle = parentForm.querySelector('.places-column__tittle')
        const inputContent = parentForm.querySelector('.places-column__content')
        inputTitle.removeAttribute('readonly')
        inputContent.removeAttribute('readonly')
    }

}

document.addEventListener('DOMContentLoaded', () => {
    /**
     * Для каждой кнопки эдита добавляет обработчик нажатия
     * и скрывает меню эдита (из карты и координат)
     */
    let editButtonList = document.querySelectorAll('.places-column__edit-button')
    editButtonList.forEach((item) => {
        const parentForm = item.parentNode.parentNode
        const submitButton = parentForm.querySelector('.places-column__save-button')
        const coordsBlock = parentForm.querySelector('.places-column__coords-manager')

        coordsBlock.style.display = 'none'
        submitButton.style.display = 'none'
        item.addEventListener('click', handleEditClick)
    })

})