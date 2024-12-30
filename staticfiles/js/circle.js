function handleSubmit() {
    // Esconder o botão
    document.getElementById("submitBtn").style.display = "none";
    
    // Mostrar o círculo de carregamento
    document.getElementById("loadingCircle").style.display = "block";
  }


function disableButtonSubmit() {
    // Esconder o botão
    document.getElementById("submitBtn").style.display = "block";
    
    // Mostrar o círculo de carregamento
    document.getElementById("loadingCircle").style.display = "none";
  }