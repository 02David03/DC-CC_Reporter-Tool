
function mountCouplingDonutGraph(canva_id, tooltip_id, data) {
  const canvas = document.getElementById(canva_id);
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
            tooltip.style.left = `${event.layerX + 10}px`;
            tooltip.style.top = `${event.layerY + 10}px`;
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

function mountCouplingGridGraph(canva_id, info_box_id, data) {
  const canvas = document.getElementById(canva_id);
  const ctx = canvas.getContext('2d');
  const infoBox = document.getElementById(info_box_id);
  const dotRadius = 5;
  const padding = 40;

  // Organizar dados para obter listas ordenadas de entradas e saídas
  const entries = Object.keys(data).map(Number).sort((a, b) => a - b);
  const outputs = [...new Set(Object.values(data).flatMap(obj => Object.keys(obj).map(Number)))].sort((a, b) => a - b);

  drawGrid(canvas, ctx, entries, outputs, padding);
  drawCouplingPoints(canvas, ctx, infoBox, dotRadius, padding, entries, outputs, data);
}

// Função para desenhar a grade
function drawGrid(canvas, ctx, entries, outputs, padding) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // Desenhar linhas pontilhadas e rótulos nos eixos
  for (let i = 0; i < entries.length; i++) {
    let y = padding + i * (canvas.height - padding * 2) / (entries.length - 1);
    ctx.strokeStyle = '#ccc';
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.moveTo(padding, y);
    ctx.lineTo(canvas.width - padding, y);
    ctx.stroke();

    ctx.fillStyle = '#000';
    ctx.fillText(entries[i], padding - 20, y + 3);
  }

  for (let j = 0; j < outputs.length; j++) {
    let x = padding + j * (canvas.width - padding * 2) / (outputs.length - 1);
    ctx.beginPath();
    ctx.moveTo(x, padding);
    ctx.lineTo(x, canvas.height - padding);
    ctx.stroke();

    ctx.fillStyle = '#000';
    ctx.fillText(outputs[j], x - 5, canvas.height - padding + 20);
  }
}

// Função para desenhar pontos de acoplamento
function drawCouplingPoints(canvas, ctx, infoBox, dotRadius, padding, entries, outputs, data) {
  for (let i = 0; i < entries.length; i++) {
    const entry = entries[i];
    for (let j = 0; j < outputs.length; j++) {
      const output = outputs[j];

      if (data[entry] && data[entry][output]) {
        let x = padding + j * (canvas.width - padding * 2) / (outputs.length - 1);
        let y = padding + i * (canvas.height - padding * 2) / (entries.length - 1);

        ctx.beginPath();
        ctx.arc(x, y, dotRadius, 0, 2 * Math.PI);
        ctx.fillStyle = '#0067B1';
        ctx.fill();

        // Adicionar dados ao ponto para interatividade
        canvas.addEventListener('mousemove', (event) => {
          const rect = canvas.getBoundingClientRect();
          const mouseX = event.clientX - rect.left;
          const mouseY = event.clientY - rect.top;
          if (Math.hypot(mouseX - x, mouseY - y) < dotRadius) {
            // Exibir tooltip com valores de acoplamento
            infoBox.style.display = 'block';
            infoBox.style.left = `${event.layerX + 10}px`;
            infoBox.style.top = `${event.layerY+ 10}px`;
            infoBox.innerHTML = `
              <strong>Entrada:</strong> ${entry}<br>
              <strong>Saída:</strong> ${output}<br>
              <strong>Valores:</strong> ${data[entry][output].join(',')}
            `;
          }
        });

        canvas.addEventListener("mouseleave", () => {
          infoBox.style.display = "none";
        });
      }
    }
  }
}

