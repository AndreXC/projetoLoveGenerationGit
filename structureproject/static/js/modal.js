document.addEventListener('DOMContentLoaded', function() {
    // Função para abrir o modal
    function openLoveModal(message, title = "Atenção") {
        const modal = document.getElementById('loveModal');
        const modalTitle = document.querySelector('.modal-title');
        const modalMessage = document.querySelector('.modal-message');

        // Atualiza o título e a mensagem
        modalTitle.textContent = title;
        modalMessage.textContent = message;

        // Exibe o modal
        modal.style.display = 'block';
    }

    // Função para fechar o modal
    function closeLoveModal() {
        const modal = document.getElementById('loveModal');
        modal.style.display = 'none';   
    }

    // Event listeners para fechar o modal
    document.querySelector('.modal-btn').addEventListener('click', closeLoveModal);
    document.querySelector('.close-btn').addEventListener('click', closeLoveModal);

    // Fecha o modal se o usuário clicar fora dele
    window.addEventListener('click', function(event) {
        const modal = document.getElementById('loveModal');
        if (event.target === modal) {
            closeLoveModal();
        }
    });

    // Expondo a função openLoveModal para que possa ser usada globalmente
    window.openLoveModal = openLoveModal;
});
