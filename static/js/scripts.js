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
    const konamiCode = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];
    let konamiCodePosition = 0;

    document.addEventListener('keydown', function (event) {
        if (event.keyCode === konamiCode[konamiCodePosition]) {
            konamiCodePosition++;
            if (konamiCodePosition === konamiCode.length) {
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

function dismissAlert(alertBox) {
    alertBox.classList.add('fade-out');
    setTimeout(function () {
        alertBox.style.display = 'none';
    }, 500);
}

function listenForIDKFA() {
    const idkfaCode = [73, 68, 75, 70, 65];
    let idkfaPosition = 0;
    let idkfaActivated = false;

    document.addEventListener('keydown', function(event) {
        if (idkfaActivated) return;
        if (event.keyCode === idkfaCode[idkfaPosition]) {
            idkfaPosition++;
            if (idkfaPosition === idkfaCode.length) {
                idkfaActivated = true;
                activateIDKFA();
                idkfaPosition = 0;
            }
        } else {
            idkfaPosition = 0;
        }
    });
}

function activateIDKFA() {
    const audio = new Audio('/static/sounds/idkfa.mp3');
    audio.play();
    setTimeout(() => {
        const overlay = document.createElement('div');
        overlay.style.position = 'fixed';
        overlay.style.top = 0;
        overlay.style.left = 0;
        overlay.style.width = '100vw';
        overlay.style.height = '100vh';
        overlay.style.background = 'rgba(255,0,0,0.3)';
        overlay.style.pointerEvents = 'none';
        overlay.style.zIndex = 9998;
        overlay.id = 'idkfa-red-overlay';
        document.body.appendChild(overlay);

        const img = document.createElement('img');
        img.src = '/static/images/idkfa.png';
        img.style.position = 'fixed';
        img.style.top = '5px';
        img.style.left = '5px';
        img.style.padding = '5px';
        img.style.zIndex = 9999;
        img.style.maxWidth = '200px';
        img.style.maxHeight = '200px';
        img.id = 'idkfa-img';
        document.body.appendChild(img);

        setTimeout(() => {
            if (img.parentNode) img.parentNode.removeChild(img);
        }, 5000);

        setTimeout(() => {
            if (overlay.parentNode) overlay.parentNode.removeChild(overlay);
        }, 25000);
    }, 0);
}

function listenForBADTIME() {
    const badtimeCode = [66, 65, 68, 84, 73, 77, 69];
    let badtimePosition = 0;
    let badtimeActivated = false;

    document.addEventListener('keydown', function(event) {
        if (badtimeActivated) return;
        if (event.keyCode === badtimeCode[badtimePosition]) {
            badtimePosition++;
            if (badtimePosition === badtimeCode.length) {
                badtimeActivated = true;
                showBadTimeBox();
                badtimePosition = 0;
            }
        } else {
            badtimePosition = 0;
        }
    });
}

function showBadTimeBox() {
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = 0;
    overlay.style.left = 0;
    overlay.style.width = '100vw';
    overlay.style.height = '100vh';
    overlay.style.background = 'rgba(0,0,0,0.85)';
    overlay.style.zIndex = 10000;
    overlay.id = 'badtime-overlay';

    const box = document.createElement('div');
    box.style.position = 'fixed';
    box.style.top = '50%';
    box.style.left = '50%';
    box.style.transform = 'translate(-50%, -50%)';
    box.style.background = '#000';
    box.style.color = '#fff';
    box.style.padding = '32px 48px';
    box.style.border = '4px solid #fff';
    box.style.borderRadius = '0';
    box.style.boxShadow = '0 0 0 8px #fff, 0 0 32px #000';
    box.style.textAlign = 'center';
    box.style.zIndex = 10001;
    box.style.fontFamily = '"Comic Sans MS", "Comic Sans", cursive, sans-serif';
    box.style.letterSpacing = '1px';
    box.style.fontSize = '1.3rem';
    box.style.maxWidth = '90vw';

    const border = document.createElement('div');
    border.style.position = 'absolute';
    border.style.top = '-8px';
    border.style.left = '-8px';
    border.style.right = '-8px';
    border.style.bottom = '-8px';
    border.style.border = '4px solid #fff';
    border.style.pointerEvents = 'none';
    box.appendChild(border);

    const text = document.createElement('div');
    text.textContent = 'Do you want to have a bad time?';
    text.style.marginBottom = '28px';
    text.style.textShadow = '2px 2px 0 #000, 0 0 8px #fff';
    box.appendChild(text);

    const btnContainer = document.createElement('div');
    btnContainer.style.display = 'flex';
    btnContainer.style.justifyContent = 'center';
    btnContainer.style.gap = '32px';

    const yesBtn = document.createElement('button');
    yesBtn.textContent = '► YES';
    yesBtn.style.padding = '10px 32px';
    yesBtn.style.background = '#000';
    yesBtn.style.color = '#fff';
    yesBtn.style.border = '2px solid #fff';
    yesBtn.style.borderRadius = '0';
    yesBtn.style.fontFamily = '"Comic Sans MS", "Comic Sans", cursive, sans-serif';
    yesBtn.style.fontSize = '1.1rem';
    yesBtn.style.cursor = 'pointer';
    yesBtn.style.textShadow = '2px 2px 0 #000, 0 0 8px #fff';
    yesBtn.onmouseover = () => { yesBtn.style.background = '#222'; };
    yesBtn.onmouseout = () => { yesBtn.style.background = '#000'; };

    const noBtn = document.createElement('button');
    noBtn.textContent = 'NO';
    noBtn.style.padding = '10px 32px';
    noBtn.style.background = '#000';
    noBtn.style.color = '#fff';
    noBtn.style.border = '2px solid #fff';
    noBtn.style.borderRadius = '0';
    noBtn.style.fontFamily = '"Comic Sans MS", "Comic Sans", cursive, sans-serif';
    noBtn.style.fontSize = '1.1rem';
    noBtn.style.cursor = 'pointer';
    noBtn.style.textShadow = '2px 2px 0 #000, 0 0 8px #fff';
    noBtn.onmouseover = () => { noBtn.style.background = '#222'; };
    noBtn.onmouseout = () => { noBtn.style.background = '#000'; };

    btnContainer.appendChild(yesBtn);
    btnContainer.appendChild(noBtn);
    box.appendChild(btnContainer);

    overlay.appendChild(box);
    document.body.appendChild(overlay);

    function closeBox() {
        if (overlay.parentNode) overlay.parentNode.removeChild(overlay);
    }

    noBtn.onclick = function() {
        closeBox();
    };

    yesBtn.onclick = function() {
        closeBox();
        switchToSansTheme();
        playMegalovania();
        startBouncingSans();
        spawnControllablePlayer();
    };
}

function switchToSansTheme() {
    let link = document.querySelector('link[rel="stylesheet"]');
    if (link) {
        link.href = '/static/css/sans.css';
    } else {
        link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '/static/css/sans.css';
        document.head.appendChild(link);
    }
}

let megalovaniaAudio = null;
function playMegalovania() {
    if (megalovaniaAudio) {
        megalovaniaAudio.pause();
        megalovaniaAudio = null;
    }
    megalovaniaAudio = new Audio('/static/sounds/megalovania.mp3');
    megalovaniaAudio.loop = true;
    megalovaniaAudio.play();
}

let sansBounceInterval = null;
let sansHitCount = 0;
function startBouncingSans() {
    if (document.getElementById('bouncing-sans')) return;

    const img = document.createElement('img');
    img.src = '/static/images/sans.gif';
    img.id = 'bouncing-sans';
    img.style.position = 'fixed';
    img.style.left = '50px';
    img.style.top = '50px';
    img.style.width = (100) + 'px';
    img.style.height = (125) + 'px';
    img.style.zIndex = 10002;
    img.style.pointerEvents = 'none';
    document.body.appendChild(img);

    let x = 50, y = 50;
    let dx = 3 + Math.random() * 2, dy = 3 + Math.random() * 2;
    let w = 100 * 0.75, h = 100 * 0.75;

    function move() {
        const ww = window.innerWidth;
        const wh = window.innerHeight;
        x += dx;
        y += dy;
        if (x <= 0 || x + w >= ww) dx = -dx;
        if (y <= 0 || y + h >= wh) dy = -dy;
        x = Math.max(0, Math.min(x, ww - w));
        y = Math.max(0, Math.min(y, wh - h));
        img.style.left = x + 'px';
        img.style.top = y + 'px';
    }

    sansBounceInterval = setInterval(move, 16);
    window.addEventListener('beforeunload', stopBouncingSans);
}

function stopBouncingSans() {
    if (sansBounceInterval) {
        clearInterval(sansBounceInterval);
        sansBounceInterval = null;
    }
    const img = document.getElementById('bouncing-sans');
    if (img && img.parentNode) img.parentNode.removeChild(img);
}

let playerInterval = null;
let playerPos = { x: 0, y: 0 };
let playerSpeed = 5;
let playerSize = 32 * 0.75;
let playerElem = null;
let playerKeys = { ArrowUp: false, ArrowDown: false, ArrowLeft: false, ArrowRight: false };
let canShoot = true;
let bullets = [];
let bulletInterval = null;

function spawnControllablePlayer() {
    if (document.getElementById('player-sprite')) return;
    playerPos.x = Math.floor((window.innerWidth - playerSize) / 2);
    playerPos.y = Math.floor((window.innerHeight - playerSize) / 2);

    playerElem = document.createElement('img');
    playerElem.id = 'player-sprite';
    playerElem.src = '/static/images/player.png';
    playerElem.style.position = 'fixed';
    playerElem.style.left = playerPos.x + 'px';
    playerElem.style.top = playerPos.y + 'px';
    playerElem.style.width = playerSize + 'px';
    playerElem.style.height = playerSize + 'px';
    playerElem.style.zIndex = 10003;
    playerElem.style.pointerEvents = 'none';
    document.body.appendChild(playerElem);

    window.addEventListener('keydown', playerKeyDown);
    window.addEventListener('keyup', playerKeyUp);

    playerInterval = setInterval(movePlayer, 16);
    bullets = [];
    canShoot = true;
    window.addEventListener('keydown', bulletKeyDown);
    if (!bulletInterval) {
        bulletInterval = setInterval(moveBullets, 16);
    }
}

function playerKeyDown(e) {
    if (e.key in playerKeys) {
        playerKeys[e.key] = true;
        e.preventDefault();
    }
}

function playerKeyUp(e) {
    if (e.key in playerKeys) {
        playerKeys[e.key] = false;
        e.preventDefault();
    }
}

function movePlayer() {
    let moved = false;
    if (playerKeys.ArrowUp) {
        playerPos.y -= playerSpeed;
        moved = true;
    }
    if (playerKeys.ArrowDown) {
        playerPos.y += playerSpeed;
        moved = true;
    }
    if (playerKeys.ArrowLeft) {
        playerPos.x -= playerSpeed;
        moved = true;
    }
    if (playerKeys.ArrowRight) {
        playerPos.x += playerSpeed;
        moved = true;
    }
    playerPos.x = Math.max(0, Math.min(window.innerWidth - playerSize, playerPos.x));
    playerPos.y = Math.max(0, Math.min(window.innerHeight - playerSize, playerPos.y));
    if (playerElem) {
        playerElem.style.left = playerPos.x + 'px';
        playerElem.style.top = playerPos.y + 'px';
    }
    if (moved) {
        checkPlayerCollision();
    }
}

function checkPlayerCollision() {
    const sans = document.getElementById('bouncing-sans');
    if (!sans || !playerElem) return;
    const sansRect = sans.getBoundingClientRect();
    const playerRect = playerElem.getBoundingClientRect();
    if (
        playerRect.left < sansRect.right &&
        playerRect.right > sansRect.left &&
        playerRect.top < sansRect.bottom &&
        playerRect.bottom > sansRect.top
    ) {
        showDeathSequence();
    }
}

function removePlayer() {
    if (playerInterval) {
        clearInterval(playerInterval);
        playerInterval = null;
    }
    window.removeEventListener('keydown', playerKeyDown);
    window.removeEventListener('keyup', playerKeyUp);
    window.removeEventListener('keydown', bulletKeyDown);
    if (playerElem && playerElem.parentNode) {
        playerElem.parentNode.removeChild(playerElem);
    }
    playerElem = null;
    bullets.forEach(b => {
        if (b.elem && b.elem.parentNode) b.elem.parentNode.removeChild(b.elem);
    });
    bullets = [];
    if (bulletInterval) {
        clearInterval(bulletInterval);
        bulletInterval = null;
    }
}

function bulletKeyDown(e) {
    if (e.repeat) return;
    if (e.key === 'z' || e.key === 'Z') {
        shootBullet();
    }
}

function shootBullet() {
    if (!canShoot || !playerElem) return;
    canShoot = false;
    setTimeout(() => { canShoot = true; }, 1000);
    const bulletSize = 4;
    const bulletSpeed = 8;
    const bullet = document.createElement('div');
    bullet.style.position = 'fixed';
    bullet.style.width = bulletSize + 'px';
    bullet.style.height = bulletSize + 'px';
    bullet.style.background = 'red';
    bullet.style.borderRadius = '2px';
    bullet.style.left = (playerPos.x + playerSize / 2 - bulletSize / 2) + 'px';
    bullet.style.top = (playerPos.y - bulletSize) + 'px';
    bullet.style.zIndex = 10004;
    bullet.className = 'player-bullet';
    document.body.appendChild(bullet);

    bullets.push({
        elem: bullet,
        x: playerPos.x + playerSize / 2 - bulletSize / 2,
        y: playerPos.y - bulletSize,
        size: bulletSize,
        speed: bulletSpeed
    });
}

function moveBullets() {
    const sans = document.getElementById('bouncing-sans');
    let sansRect = null;
    if (sans) sansRect = sans.getBoundingClientRect();
    for (let i = bullets.length - 1; i >= 0; i--) {
        const b = bullets[i];
        b.y -= b.speed;
        if (b.elem) {
            b.elem.style.top = b.y + 'px';
        }
        if (b.y + b.size < 0) {
            if (b.elem && b.elem.parentNode) b.elem.parentNode.removeChild(b.elem);
            bullets.splice(i, 1);
            continue;
        }
        if (sans && sansRect) {
            const bx = b.x, by = b.y, bs = b.size;
            if (
                bx < sansRect.right &&
                bx + bs > sansRect.left &&
                by < sansRect.bottom &&
                by + bs > sansRect.top
            ) {
                if (b.elem && b.elem.parentNode) b.elem.parentNode.removeChild(b.elem);
                bullets.splice(i, 1);
                incrementSansHit();
            }
        }
    }
}

function incrementSansHit() {
    sansHitCount = (sansHitCount || 0) + 1;
    if (sansHitCount >= 10) {
        winSequence();
    }
}

function winSequence() {
    if (megalovaniaAudio) {
        megalovaniaAudio.pause();
        megalovaniaAudio = null;
    }
    stopBouncingSans();
    removePlayer();
    const overlays = ['badtime-overlay', 'ut-death-black-overlay', 'ut-death-video'];
    overlays.forEach(id => {
        const el = document.getElementById(id);
        if (el && el.parentNode) el.parentNode.removeChild(el);
    });
    window.location.href = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ&start_radio=1';
}

function showDeathSequence() {
    if (megalovaniaAudio) {
        megalovaniaAudio.pause();
        megalovaniaAudio = null;
    }
    stopBouncingSans();
    removePlayer();
    const blackOverlay = document.createElement('div');
    blackOverlay.style.position = 'fixed';
    blackOverlay.style.top = 0;
    blackOverlay.style.left = 0;
    blackOverlay.style.width = '100vw';
    blackOverlay.style.height = '100vh';
    blackOverlay.style.background = '#000';
    blackOverlay.style.zIndex = 20000;
    blackOverlay.id = 'ut-death-black-overlay';
    document.body.appendChild(blackOverlay);

    const video = document.createElement('video');
    video.src = '/static/videos/ut_death.mp4';
    video.style.position = 'fixed';
    video.style.top = '50%';
    video.style.left = '50%';
    video.style.transform = 'translate(-50%, -50%)';
    video.style.zIndex = 20001;
    video.style.maxWidth = '100vw';
    video.style.maxHeight = '100vh';
    video.autoplay = true;
    video.playsInline = true;
    video.id = 'ut-death-video';
    document.body.appendChild(video);

    let cleanedUp = false;
    function cleanupDeath() {
        if (cleanedUp) return;
        cleanedUp = true;
        if (video && video.parentNode) video.parentNode.removeChild(video);
        if (blackOverlay && blackOverlay.parentNode) blackOverlay.parentNode.removeChild(blackOverlay);
        revertToDefaultTheme();
    }

    video.onended = cleanupDeath;
    setTimeout(cleanupDeath, 20000);
}

function revertToDefaultTheme() {
    let link = document.querySelector('link[rel="stylesheet"]');
    if (link) {
        link.href = '/static/css/halo.css';
    } else {
        link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '/static/css/halo.css';
        document.head.appendChild(link);
    }
}
x
listenForBADTIME();
listenForKonamiCode();
listenForIDKFA();
