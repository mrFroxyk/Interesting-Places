/**
 * Скрипт для авторизации через вк, создает кнопку авторизации
 */

document.addEventListener("DOMContentLoaded", function () {
    const VKID = window.VKIDSDK;
    VKID.Config.set({
        app: 51926680, // Идентификатор приложения.
        redirectUrl: "https://sabaton-enjoyer.online/auth", // Адрес для перехода после авторизации.
        state: 'dj29fnsadjsd82' // Произвольная строка состояния приложения.
    });

    const oneTap = new VKID.OneTap();
    const container = document.getElementById('VkIdSdkOneTap');
    if (container) {
        oneTap.render({container: container, scheme: VKID.Scheme.LIGHT, lang: VKID.Languages.RUS});
    } else {
        console.log("Ошибка: не найден контейнер для монтирования кнопки аунтификации")
    }
});