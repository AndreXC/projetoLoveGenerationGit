// Função para gerar corações flutuantes com emoji
const heartsContainer = document.querySelector('.hearts');
let heartCount = 0; // Contador de corações
const maxHearts = 150; // Número máximo de corações na tela

function createHeart() {
    if (heartCount < maxHearts) {
        const heart = document.createElement('div');
        heart.classList.add('heart_animation');
        heart.innerText = '❤️'; // Emoji de coração
        heart.style.left = `${Math.random() * 100}vw`; // Posição horizontal aleatória
        heart.style.fontSize = `${Math.random() * 20 + 15}px`; // Tamanho aleatório do emoji
        heart.style.bottom = `0`; // Começar na parte inferior da tela
        heart.style.animationDuration = `${Math.random() * 3 + 2}s`; // Duração aleatória da animação
        heartsContainer.appendChild(heart);

        // Incrementar contador
        heartCount++;

        // Remove o coração após a animação
        heart.addEventListener('animationend', () => {
            heart.remove();
            heartCount--; // Decrementar o contador ao remover
        });
    } else {
        resetHearts(); // Resetar corações se atingir o máximo
    }
}

// Função para redefinir os corações
function resetHearts() {
    heartsContainer.innerHTML = ''; // Limpa todos os corações
    heartCount = 0; // Reinicia o contador
}

// Gerar um coração a cada 300ms
setInterval(createHeart, 100);
