// Seleciona todas as caixas de flores
const flowerBoxes = document.querySelectorAll('.flower-box');

// Adiciona evento de clique para cada caixa de flor
flowerBoxes.forEach(box => {
    box.addEventListener('click', () => {
        // Remove a seleção de todas as caixas
        flowerBoxes.forEach(b => b.classList.remove('selected'));
        // Adiciona a classe de seleção à caixa clicada
        box.classList.add('selected');
    });
});
