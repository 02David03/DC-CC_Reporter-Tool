
function mountDonutCouplingGraph(el_id, tooltip_id, data) {
  const canvas = document.getElementById(el_id);
  const ctx = canvas.getContext("2d");

  const labels = ["Entradas acopladas", "Entradas não identificaveis"];
  const colors = ["#0a1a5c", "#6E6E6E"]; // Cores
  const total = data.reduce((acc, val) => acc + val, 0); // Soma dos valores
  
  // Configurações do gráfico
  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;
  const radius = canvas.width / 2;
  const innerRadius = canvas.width / 4;

  // Variável para acompanhar o ângulo atual
  let startAngle = 0.5 * Math.PI; // Início no eixo Y (90 graus)

  data.forEach((value, index) => {
    // Calcula o ângulo final
    const sliceAngle = (value / total) * 2 * Math.PI;
  
    // Desenha o arco (parte do donut)
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, radius, startAngle, startAngle + sliceAngle);
    ctx.closePath();
    ctx.fillStyle = colors[index];
    ctx.fill();
  
    // Atualiza o ângulo inicial
    startAngle += sliceAngle;
  });
  
  // Desenha o círculo interno para criar o "furo"
  ctx.beginPath();
  ctx.arc(centerX, centerY, innerRadius, 0, 2 * Math.PI);
  ctx.fillStyle = "#ffffff"; // Cor do círculo interno (fundo)
  ctx.fill();


  // Tooltip 
  const tooltip = document.getElementById(tooltip_id);
  canvas.addEventListener("mousemove", function (event) {
    const rect = canvas.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;
  
    const dx = mouseX - centerX;
    const dy = mouseY - centerY;
    const distance = Math.sqrt(dx * dx + dy * dy);
  
    if (distance >= innerRadius && distance <= radius) {
      // Calcula o ângulo do mouse
      let angle = Math.atan2(dy, dx);
      if (angle < 0.5 * Math.PI) {
        angle += 2 * Math.PI; // Ajusta para o intervalo de [0, 2PI]
      }
  
      // Determina qual fatia está sendo "hovered"
      let currentAngle = 0.5 * Math.PI;
      for (let i = 0; i < data.length; i++) {
        const sliceAngle = (data[i] / total) * 2 * Math.PI;
        if (angle >= currentAngle && angle < currentAngle + sliceAngle) {
           // Atualiza o conteúdo e posição do tooltip
            tooltip.style.display = "block";
            tooltip.style.left = `${event.clientX + 10}px`;
            tooltip.style.top = `${event.clientY + 10}px`;
            tooltip.innerHTML = `
              <strong>${labels[i]}</strong><br>
              ${data[i]}
            `;
          return;
        }
        currentAngle += sliceAngle;
      }
    } else {
      tooltip.style.display = "none"; // Esconde o tooltip quando fora do gráfico
    }
  });

  // Esconde o tooltip quando o mouse sai do canvas
  canvas.addEventListener("mouseleave", () => {
    tooltip.style.display = "none";
  });
}


