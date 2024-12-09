document.getElementById('loveForm').addEventListener('submit', function (e) {
    e.preventDefault(); 
    const images = document.getElementById('fileInput').files;
    const nome = document.getElementById('nome').value.trim();
    const Email = document.getElementById('email').value.trim();
    const mensagem = document.getElementById('mensagem').value.trim();
    const service = document.querySelector('input[name="service"]:checked');
    const selectedFlower = document.querySelector('.flower-box.selected')?.getAttribute('data-flower') || '';
    const CheckboxDateHour = document.getElementById('addDateTime').checked;
    const date = document.getElementById('dateInput').value.trim();
    const hour = document.getElementById('timeInput').value.trim();

    // Array para armazenar mensagens de erro
    let errors = [];
    const allowedFormats = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/svg+xml'];
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    // Validação dos campos
    if (!nome) errors.push('❌ Nome do parceiro(a) é obrigatório!');
    if (!Email) errors.push('❌ Campo (Email) é obrigatório!');
    if (!emailRegex.test(Email)) errors.push('❌ Campo (Email) esta no formato incorreto ou errado!')
    if (!mensagem) errors.push('❌ Mensagem de amor é obrigatória!');
    if (!service) errors.push('❌ Escolha um serviço!');
    if (!selectedFlower) errors.push('🌸 Selecione uma Flor!');
    if (images.length === 0) errors.push('📸 Adicione pelo menos uma imagem (imagem do parceiro/a)!');
    if (images.length > 5) errors.push('📸 Limite de fotos, suba até no maximo 5 fotos!');
    for (let i = 0; i < images.length; i++) {;
        if (!allowedFormats.includes(images[i].type)) {
            errors.push(`❌ O arquivo "${images[i].name}" não é um formato válido. Aceitamos apenas JPEG, JPG, PNG, GIF ou SVG.`);
        }
    }

    // Se houver erros, exibir o modal apropriado
    if (errors.length > 0) {
        const errorMessage = `Os campos a seguir não foram preenchidos ou estão incorretos!:\n${errors.join(', ')}`;
        openLoveModal(errorMessage, "Preencha os Dados");
        return; // Interrompe o envio se houver erros
    }
    const formData = new FormData(this);
    formData.append('nome', nome);
    formData.append('email', Email);
    formData.append('mensagem', mensagem);
    formData.append('service', service.value);
    formData.append('flower', selectedFlower);
    
    if (CheckboxDateHour) {
        formData.append('date', date);
        formData.append('hour', hour);
    }
    else {
        formData.append('date', '');
        formData.append('hour', '');
    }
    for (let i = 0; i < images.length; i++) {
        formData.append('images[]', images[i]);
    }
    
    //chamar o Circle carregamento antes de iniciar o action
    handleSubmit();
    // Envia o formulário com fetch, usando o método POST explicitamente
    fetch(this.action, {
        method: 'POST',  // Especifica explicitamente o método POST
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    }).then(response => {
        return response.json(); // Captura a resposta como JSON
    }).then(data => {
        if (data.status === 'success') {
            // Redireciona para a URL fornecida na resposta
             window.location.href = data.redirect_url; // Redireciona para a URL desejada
        } else {
            openLoveModal('Estamos com problema em nosso Servido, tente novamente mais tarde', "Erro");
            disableButtonSubmit()
        }
    }).catch(error => {
        console.error("Erro na requisição:", error);
        openLoveModal('Estamos com problema em nosso Servido, tente novamente mais tarde', "Erro");
        disableButtonSubmit();
    });
});
