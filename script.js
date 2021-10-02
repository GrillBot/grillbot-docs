window.onload = () => {
    setTitle();
    setLoadDate();
};

const setTitle = () => {
    const header = document.body.getElementsByTagName('h1');
    if (header.length == 0) return;

    document.title = header[0].innerText;
};

const setLoadDate = () => {
    const elements = document.body.getElementsByClassName('now-date');
    if (elements.length == 0) return;

    const now = getFormatedNowDateTime();
    for (const element of elements) {
        element.innerHTML = now;
    }
};

const getFormatedNowDateTime = () => {
    const now = new Date();
    return `${now.getDay()}. ${now.getMonth()}. ${now.getFullYear()} ${now.getHours()}:${now.getMinutes()}:${now.getSeconds()}`;
};
