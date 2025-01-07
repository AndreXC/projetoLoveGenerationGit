// Função para validar o tipo de arquivo
function isValidFileType(file) {
    const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/jpg'];
    return validTypes.includes(file.type);
}

// Função para remover um arquivo da lista
function removeFile(listItem, fileInput, fileIndex) {
    listItem.remove(); // Remove o item da lista

    // Cria um novo DataTransfer para manipular os arquivos restantes
    const dt = new DataTransfer();
    Array.from(fileInput.files).forEach((file, index) => {
        if (index !== fileIndex) {
            dt.items.add(file); // Adiciona os arquivos que não foram removidos
        }
    });

    fileInput.files = dt.files; // Atualiza os arquivos no input
}

// Evento de clique para abrir o seletor de arquivos
document.querySelector('.dropzone').addEventListener('click', function () {
    document.getElementById('fileInput').click(); // Abre o seletor de arquivos ao clicar no dropzone
});

// Evento de alteração no seletor de arquivos
document.getElementById('fileInput').addEventListener('change', function (e) {
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = ''; // Limpa a lista

    Array.from(e.target.files).forEach((file, index) => {
        if (isValidFileType(file)) {
            const listItem = document.createElement('li');
            listItem.textContent = file.name; // Exibe o nome do arquivo

            // Cria o botão "X" para remover o arquivo
            const removeButton = document.createElement('button');
            removeButton.textContent = 'X';
            removeButton.classList.add('remove-file');
            removeButton.addEventListener('click', function (event) {
                event.stopPropagation(); // Evita abrir o seletor de arquivos
                removeFile(listItem, e.target, index); // Remove o arquivo ao clicar no "X"
            });

            listItem.appendChild(removeButton); // Adiciona o botão "X" ao item da lista
            fileList.appendChild(listItem);
        } else {
            openLoveModal("Os arquivos a serem carregados precisam ser do tipo .jpg, .jpeg, .png, ou .gif", "Erro");
        }
    });
});

// Evento de arrastar sobre o dropzone
document.querySelector('.dropzone').addEventListener('dragover', function (e) {
    e.preventDefault();
    this.classList.add('active'); // Adiciona uma classe "active" enquanto arrasta o arquivo
});

// Evento de sair da área do dropzone
document.querySelector('.dropzone').addEventListener('dragleave', function () {
    this.classList.remove('active'); // Remove a classe "active" ao sair
});

// Evento de soltar arquivos no dropzone
document.querySelector('.dropzone').addEventListener('drop', function (e) {
    e.preventDefault();
    this.classList.remove('active'); // Remove a classe "active" após soltar o arquivo

    const files = e.dataTransfer.files;
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = ''; // Limpa a lista

    Array.from(files).forEach((file, index) => {
        if (isValidFileType(file)) {
            const listItem = document.createElement('li');
            listItem.textContent = file.name; // Exibe o nome do arquivo

            // Cria o botão "X" para remover o arquivo
            const removeButton = document.createElement('button');
            removeButton.textContent = 'X';
            removeButton.classList.add('remove-file');
            removeButton.addEventListener('click', function (event) {
                event.stopPropagation(); // Evita abrir o seletor de arquivos
                removeFile(listItem, document.getElementById('fileInput'), index); // Remove o arquivo ao clicar no "X"
            });

            listItem.appendChild(removeButton); // Adiciona o botão "X" ao item da lista
            fileList.appendChild(listItem);
        } else {
            openLoveModal("Os arquivos a serem carregados precisam ser do tipo .jpg, .jpeg, .png, ou .gif", "Erro");
        }
    });
});
