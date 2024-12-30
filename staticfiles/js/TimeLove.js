function calculateTimeDifference(data, hour) {
  // Monta a string de data e hora no formato ISO
  const targetDateTime = `${data}T${hour}:00`;
  const targetDate = new Date(targetDateTime);

  function updateDifference() {
    const now = new Date();
    const diffInMillis = now - targetDate;

    // Convertendo para dias, horas, minutos e segundos
    const totalSeconds = Math.floor(diffInMillis / 1000);
    const days = Math.floor(totalSeconds / 86400);
    const hours = Math.floor((totalSeconds % 86400) / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    // Atualizando o conteúdo no HTML
    const timeDisplay = document.getElementById('time-display');
    timeDisplay.textContent = `${days} dias, ${hours} horas, ${minutes} minutos e ${seconds} segundos`;
  }

  // Atualiza o cálculo a cada segundo
  setInterval(updateDifference, 1000);

  // Executa imediatamente no início
  updateDifference();
}

