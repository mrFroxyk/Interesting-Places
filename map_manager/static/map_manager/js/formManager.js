ymaps.ready(init);

let isPlaceMarkCreated = false
let balun = null // контейнер, куда положим балун синглтон
let mapWithPlaces = null;
let memoryCoords = null;


function init() {
    mapWithPlaces = new ymaps.Map("formMap", {
        center: [55.76, 37.64],
        zoom: 5
    });

    mapWithPlaces.controls.add('zoomControl');
    mapWithPlaces.controls.add('typeSelector');
    mapWithPlaces.controls.add('searchControl');

    mapWithPlaces.events.add('click', function (e) {
        let coords = e.get('coords');
        actionAfterPlaceMarkChangePos(coords)
    });
}

function addPlaceMark(coords) {
    balun = new ymaps.Placemark(coords, {
        iconContent: 'Место для воспоминания',
    }, {
        balloonPanelMaxMapArea: 0,
        draggable: "true",
        preset: "islands#blueStretchyIcon",
    })

    balun.events.add('dragend', function (e) {
        let coords = balun.geometry.getCoordinates();
        actionAfterPlaceMarkChangePos(coords)
    });

    mapWithPlaces.geoObjects.add(balun);
}

function actionAfterPlaceMarkChangePos(coords) {
    /**
     * При любом изменении позици балуна измененяет координаты
     * в памяти
     */

    if (isPlaceMarkCreated) {
        mapWithPlaces.panTo(coords, {duration: 500});
        balun.geometry.setCoordinates(coords);
    } else {
        addPlaceMark(coords)
        isPlaceMarkCreated = true
    }
    setCoords(coords)
    memoryCoords = coords
}

function setCoords(coords) {
    /**
     * Рендерит координаты внутри формы и сохраняет их в
     * в DOM дереве
     */
    const firstCoordDom = document.querySelector('.input-form__coords1')
    const secondCoordDom = document.querySelector('.input-form__coords2')
    firstCoordDom.value = coords[0]
    secondCoordDom.value = coords[1]
}

function openForm() {
    /**
     * Рендерит первым элементов форму, где можно создать
     * воспоминание
     */
    inputForm.style.display = 'block';
    scrollArea.scroll(10, 10)
}

function closeForm() {
    /**
     * Закрывает форму (визуально она пропадает
     */
    inputForm.style.display = 'none';
}

let inputForm = null
let newMemoriesButton = null
let closeButton = null
let submitButton = null
let htmlForm = null;
let scrollArea = null;

window.onload = () => {
    inputForm = document.getElementById("inputForm")
    htmlForm = document.querySelector('.input-form')
    newMemoriesButton = document.getElementById('new-memories-button')
    closeButton = document.querySelector('.close-button')
    submitButton = document.querySelector('.input-form__submit-button')
    scrollArea = document.querySelector('.places-column')

    const errorMessageCloseButton = document.querySelector(".error_message__close-button")
    const errorMessage = document.querySelector(".error_message")
    errorMessageCloseButton.addEventListener('click', () => {
        errorMessage.style.display = 'none'
    })
    closeForm()

    newMemoriesButton.addEventListener('click', () => {
        openForm()
    })

    closeButton.addEventListener('click', () => {
        closeForm()
    })

    htmlForm.onsubmit = (event) => {
        event.preventDefault()
        if (validateInputData()) {
            event.currentTarget.submit()
        } else {
            errorMessage.style.display = 'flex'
        }
    }
}

function validateInputData() {
    /**
     * Валидирует данные, введенные юзером, в будущем должно
     * 1) выводить подсказки, что не так
     * 2) проверять наличие заголовка и тип файла
     */
    console.log(memoryCoords)
    return !!memoryCoords;
}

