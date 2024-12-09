// Função para realizar a busca no Django backend
function searchOrder() {
    const input = document.getElementById("search-input").value;

    // Se o input estiver vazio, não faz a busca
    if (input.trim() === "") {
        document.getElementById("result-container").style.display = "none";
        return;
    }

    // Mostrar o spinner de carregamento
    document.getElementById("loading-spinner").style.display = "block";
    document.getElementById("result-container").style.display = "none";  // Esconde o resultado enquanto carrega

    // Fazendo o request para o Django backend
    fetch(`/api/search_produto/?id=${input}`, {
        method: 'GET',
    })
        .then(response => response.json())
        .then(data => {
            // Esconde o spinner de carregamento após a resposta
            document.getElementById("loading-spinner").style.display = "none";

            // Mostra o container de resultados
            const resultContainer = document.getElementById("result-container");
            const orderInfo = document.getElementById("order-info");

            if (data && data.order) {
                // Exibe as informações do pedido
                orderInfo.innerHTML = `
                <strong>Status:</strong> ${data.order.status} <br>
                <strong>ID Cliente:</strong> ${data.order.clienteId} <br>
                <strong>Data Criação</strong> ${data.order.gerado}
                `;
                resultContainer.style.display = "block";

                if (data.order.qrcode) {
                    document.getElementById('qrcode-container').style.visibility = 'visible'
                    // Cria a imagem a partir do base64
                    const qrcodeImage = "data:image/png;base64," + data.order.qrcode;
                    document.getElementById("qrcode-image").src = qrcodeImage;
                    // Link para download
                    document.getElementById("download-link").href = qrcodeImage;
                }

            } else {
                // Caso o pedido não exista
                orderInfo.innerHTML = "Pedido não encontrado.";
                resultContainer.style.display = "block";
            }
        })
        .catch(error => {
            console.error('Erro ao buscar o pedido:', error);
            alert('Ocorreu um erro. Tente novamente mais tarde.');
            // Esconde o spinner de carregamento se houver erro
            document.getElementById("loading-spinner").style.display = "none";
        });
}
