$(document).ready(function () {
    var envelope = $('#envelope');
    var btn_open = $("#open");
    var btn_reset = $("#reset");
    var modal = $("#loveModal");
    var closeModalBtn = $("#closeModal");
  
    envelope.click(function () {
      openEnvelope();
      setTimeout(() => openModal(), 1000); // Delay para o modal sincronizar com a animação da carta
    });
  
    btn_open.click(function () {
      openEnvelope();
      setTimeout(() => openModal(), 1000);
    });
  
    btn_reset.click(function () {
      closeEnvelope();
    });
  
    closeModalBtn.click(function () {
      closeModal();
      setTimeout(() => closeEnvelope(), 300); // Pequeno atraso para suavizar a transição
    });
  
    function openEnvelope() {
      envelope.addClass("open").removeClass("close");
    }
  
    function closeEnvelope() {
      envelope.addClass("close").removeClass("open");
    }
  
    function openModal() {
      modal.removeClass("hidden").addClass("visible");
    }
  
    function closeModal() {
      modal.removeClass("visible").addClass("hidden");
    }
  });
  