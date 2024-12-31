// Atualiza o preço selecionado
const serviceOptions = document.querySelectorAll('input[name="service"]');
const priceDisplay = document.createElement('p'); // Cria um elemento para exibir o preço
priceDisplay.id = 'priceDisplay';
priceDisplay.innerText = 'Preço: R$ 8,00'; // Preço padrão
document.querySelector('.service-selection').appendChild(priceDisplay);

// Função para atualizar o preço
function updatePrice() {
    const selectedService = document.querySelector('input[name="service"]:checked').value;
    priceDisplay.innerText = `Preço: R$ ${selectedService},00`;
}

// Adiciona evento para mudar o preço ao selecionar uma opção
serviceOptions.forEach(option => {
    option.addEventListener('change', updatePrice);
});
