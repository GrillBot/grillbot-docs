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

    const day = now.getDate().toString().padStart(2, '0');
    const month = (now.getMonth() + 1).toString().padStart(2, '0');
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');

    return `${day}. ${month}. ${now.getFullYear()} ${hours}:${minutes}:${seconds}`;
};
