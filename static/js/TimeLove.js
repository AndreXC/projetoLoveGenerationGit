function calculateTimeDifference(data, hour) {
  // Monta a string de data e hora no formato ISO
  const targetDateTime = `${data}T${hour}:00`;
  const targetDate = new Date(targetDateTime);

  function updateDifference() {
    const now = new Date();
    const diffInMillis = now - targetDate;

    // Convertendo para segundos totais
    const totalSeconds = Math.floor(diffInMillis / 1000);

    // Calculando o tempo com base na diferença
    let years = 0;
    let days = Math.floor(totalSeconds / 86400);
    let remainingSeconds = totalSeconds % 86400;

    if (days >= 365) {
      years = Math.floor(days / 365);
      days = days % 365;
    }

    const hours = Math.floor(remainingSeconds / 3600);
    remainingSeconds %= 3600;
    const minutes = Math.floor(remainingSeconds / 60);
    const seconds = remainingSeconds % 60;

    // Atualizando o conteúdo no HTML
    const timeDisplay = document.getElementById('time-display');
    const containerResponsive = document.getElementById('containerNamoroResponsive');
    const timedisplayResponsive =  document.getElementById('time-display_responsivo');
    if (years > 0) {
        timedisplayResponsive.textContent = `${years} ano${years > 1 ? 's' : ''}, ${days} dia${days > 1 ? 's' : ''}, ${hours} hora${hours > 1 ? 's' : ''}, ${minutes} minuto${minutes > 1 ? 's' : ''} e ${seconds} segundo${seconds > 1 ? 's' : ''}`;
        timeDisplay.textContent = `${years} ano${years > 1 ? 's' : ''}, ${days} dia${days > 1 ? 's' : ''}, ${hours} hora${hours > 1 ? 's' : ''}, ${minutes} minuto${minutes > 1 ? 's' : ''} e ${seconds} segundo${seconds > 1 ? 's' : ''}`;
      
    } else {
        timedisplayResponsive.textContent = `${days} dia${days > 1 ? 's' : ''}, ${hours} hora${hours > 1 ? 's' : ''}, ${minutes} minuto${minutes > 1 ? 's' : ''} e ${seconds} segundo${seconds > 1 ? 's' : ''}`;
        timeDisplay.textContent = `${days} dia${days > 1 ? 's' : ''}, ${hours} hora${hours > 1 ? 's' : ''}, ${minutes} minuto${minutes > 1 ? 's' : ''} e ${seconds} segundo${seconds > 1 ? 's' : ''}`;

    }
  }

  // Atualiza o cálculo a cada segundo
  setInterval(updateDifference, 1000);
  

  // Executa imediatamente no início
  updateDifference();
}
