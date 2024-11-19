
function mountCouplingDonutGraph(canva_id, tooltip_id, data, is_component=false) {
  const canvas = document.getElementById(canva_id);
  const ctx = canvas.getContext("2d");

  const labels = !is_component ? 
    ["Entradas acopladas:", "Entradas não analisadas:", "Entradas sem identificação<br> de acoplamento:"] 
    : ["Saídas de complemento <br>acoplados:", "Saídas de complemento sem <br>identificação de acoplamento:"];
  const colors = !is_component ? ["#0a1a5c", "#6E6E6E", "#BF6A02"] : ["#0a1a5c", "#BF6A02"];
  const total = data.reduce((acc, val) => acc + val, 0);
  
  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;
  const radius = canvas.width / 2;
  const innerRadius = canvas.width / 4;

  let startAngle = 0.5 * Math.PI; 

  data.forEach((value, index) => {
    const sliceAngle = (value / total) * 2 * Math.PI;
  
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, radius, startAngle, startAngle + sliceAngle);
    ctx.closePath();
    ctx.fillStyle = colors[index];
    ctx.fill();
  
    startAngle += sliceAngle;
  });
  
  ctx.beginPath();
  ctx.arc(centerX, centerY, innerRadius, 0, 2 * Math.PI);
  ctx.fillStyle = "#ffffff"; 
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
      let angle = Math.atan2(dy, dx);
      if (angle < 0.5 * Math.PI) {
        angle += 2 * Math.PI; 
      }
  
      let currentAngle = 0.5 * Math.PI;
      for (let i = 0; i < data.length; i++) {
        const sliceAngle = (data[i] / total) * 2 * Math.PI;
        if (angle >= currentAngle && angle < currentAngle + sliceAngle) {
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
      tooltip.style.display = "none"; 
    }
  });

  canvas.addEventListener("mouseleave", () => {
    tooltip.style.display = "none";
  });
}

function mountCouplingGridGraph(canva_id, info_box_id, data, is_component = false) {
  const canvas = document.getElementById(canva_id);
  const ctx = canvas.getContext('2d');
  const infoBox = document.getElementById(info_box_id);
  const dotRadius = 5;
  const padding = 40;
  
  const entries = Object.keys(data).map(String).sort().reverse();
  const outputs = 
  !is_component ? [...new Set(
    Object.values(data)
      .flatMap(obj => Object.keys(obj).map(String))
      .filter(key => key !== 'analysed')
  )].sort():
  [...new Set( Object.values(data).flatMap(obj => obj['sut_outputs'].map(String)) )].sort();

  drawGrid(canvas, ctx, entries, outputs, padding, is_component);
  drawCouplingPoints(canvas, ctx, infoBox, dotRadius, padding, entries, outputs, data, is_component);
}

function drawGrid(canvas, ctx, entries, outputs, padding, is_component) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  for (let i = 0; i < entries.length; i++) {
    let y = padding + i * (canvas.height - padding * 2) / ((entries.length === 1 ? 2 : entries.length) - 1);
    ctx.strokeStyle = '#ccc';
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.moveTo(padding, y);
    ctx.lineTo(canvas.width - padding, y);
    ctx.stroke();

    ctx.fillStyle = '#000';
    ctx.fillText(entries[i], padding - 20, y + 3);
    if(i === 0) {
      ctx.fillText((is_component ? 'Saídas do Componente' : 'Entradas'), padding - 25, y - 20);
    }
  }

  for (let j = 0; j < outputs.length; j++) {
    let x = padding + j * (canvas.width - padding * 2) / ((outputs.length === 1 ? 2 : outputs.length) - 1);
    ctx.beginPath();
    ctx.moveTo(x, padding);
    ctx.lineTo(x, canvas.height - padding);
    ctx.stroke();

    ctx.fillStyle = '#000';
    ctx.fillText(outputs[j], x - 5, canvas.height - padding + 20);
    if(j === outputs.length - 1) {
      ctx.fillText('Saídas', x - 10, canvas.height - padding + 35);
    }
  }
}

function drawCouplingPoints(canvas, ctx, infoBox, dotRadius, padding, entries, outputs, data, is_component) {
  console.log(entries);
  console.log(outputs);
  for (let i = 0; i < entries.length; i++) {
    const entry = entries[i];
    for (let j = 0; j < outputs.length; j++) {
      const output = outputs[j];
      let shouldDraw = !is_component ? data[entry] && data[entry][output] : data[entry] && data[entry]['sut_outputs'].includes(output);
      if (shouldDraw) {
        let x = padding + j * (canvas.width - padding * 2) / ((outputs.length === 1 ? 2 : outputs.length) - 1);
        let y = padding + i * (canvas.height - padding * 2) / ((entries.length === 1 ? 2 : entries.length) - 1);

        ctx.beginPath();
        ctx.arc(x, y, dotRadius, 0, 2 * Math.PI);
        ctx.fillStyle = '#0067B1';
        ctx.fill();
        
        canvas.addEventListener('mousemove', (event) => {
          const rect = canvas.getBoundingClientRect();
          const mouseX = event.clientX - rect.left;
          const mouseY = event.clientY - rect.top;
          if (Math.hypot(mouseX - x, mouseY - y) < dotRadius) {
            infoBox.style.display = 'block';
            infoBox.style.left = `${event.layerX + 10}px`;
            infoBox.style.top = `${event.layerY + 10}px`;
            infoBox.innerHTML = `
              <strong>Entrada:</strong> ${entry}<br>
              <strong>Saída:</strong> ${output}<br>
              ${
                !is_component
                  ? `<strong>Testes de análise: <br></strong> 
                    ${data[entry][output]
                      .map(testes => `teste ${testes[0]} <=> teste ${testes[1]}`)
                      .join('<br>')}`
                  : data[entry]['forced']
                  ? '<strong class="fc-error">Valor forçado<br></strong>'
                  : ''
              }
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

