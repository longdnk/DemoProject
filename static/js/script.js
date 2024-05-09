const handleClick = event => {
    const url = new URL(location);
    url.searchParams.set('tab', event.currentTarget.value.toString());
    return history.pushState({}, '', url);
}

const handleChecked = () => {
    return window.addEventListener('load', () => {
        const tabFiles = document.getElementById('tab1');
        const tabImage = document.getElementById('tab2');
        const isFiles = location.search === "" || location.search.includes('File');
        if (isFiles) {
            tabFiles.setAttribute('checked', 'true');
            tabImage.removeAttribute('checked');
        } else {
            tabImage.setAttribute('checked', 'true');
            tabFiles.removeAttribute('checked');
        }
        if (location.search === "") {
            const url = new URL(location);
            url.searchParams.set('tab', 'File');
            return history.pushState({}, '', url);
        }
    })
}