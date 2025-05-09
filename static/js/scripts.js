function toggleThemeMenu() {
    const menu = document.getElementById('themeMenu');
    menu.classList.toggle('show');
}

window.onclick = function(e) {
    if (!e.target.closest('.dropdown')) {
        const dropdowns = document.getElementsByClassName("dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
            dropdowns[i].classList.remove('show');
        }
    }
}

function listenForKonamiCode() {
    const konamiCode = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65]; // Up, Up, Down, Down, Left, Right, Left, Right, B, A
    let konamiCodePosition = 0;

    document.addEventListener('keydown', function (event) {
        if (event.keyCode === konamiCode[konamiCodePosition]) {
            konamiCodePosition++;
            if (konamiCodePosition === konamiCode.length) {
                // Konami code successfully entered
                activateKonamiCode();
                konamiCodePosition = 0;
            }
        } else {
            konamiCodePosition = 0;
        }
    });
}

function activateKonamiCode() {
    window.open('https://youtu.be/SiJie3Z7DG8?t=129', '_blank');
}

listenForKonamiCode();