document.addEventListener('DOMContentLoaded', function() {
    // Seleciona os elementos
    const openModalBtn = document.getElementById("IconTimeLoveOpen");
    const closeModalBtn = document.getElementById("CloseLoveModalTimerLoveTimer");
    const modal = document.getElementById("LoveModalTimerLoveTimer");

    // Abre o modal ao clicar na div
    openModalBtn.addEventListener("click", () => {
        modal.style.display = "flex";
    });

    // Fecha o modal ao clicar no botão de fechar
    closeModalBtn.addEventListener("click", () => {
        modal.style.display = "none";
    });

    // Fecha o modal ao clicar fora do conteúdo
    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
    });