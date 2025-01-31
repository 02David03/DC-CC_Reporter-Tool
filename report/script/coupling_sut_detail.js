const couplingSUT = json_data.coupling_SUT;

mountAnalysesGRN0();
mountInputsTable();

function mountAnalysesGRN0() {
  let graphData = [0, 0, 0];
  for(const key in couplingSUT) {
    const subObj = couplingSUT[key];
    if(!subObj['analysed']) {
      graphData[1]++
    } else {
      let hasAnyValue = false;
      Object.entries(subObj).forEach(entry => {
        if(entry[0] !== "analysed" && entry[1] !== null && entry[1].length > 0) hasAnyValue = true;
      })
      if(hasAnyValue) {
        graphData[0]++
      } else {
        graphData[2]++
      }
    }
  }
  mountCouplingDonutGraph("GRN0-donut-graph", "GRN0-tooltip", graphData);
  mountCouplingGridGraph("GRN0-grid-graph", "GRN0-info-box", couplingSUT);
}


function mountInputsTable() {
  insertInputsCelCol();
  let outputArr = [];
  Object.values(couplingSUT).forEach(value => {
    outputArr = [...new Set([...(Object.keys(value)), ...outputArr])].filter(key => key !== 'analysed');
  });
  outputArr = outputArr.sort();
  insertOutputsSubHeadCelArray(outputArr);
  insertOutputsTableCelArray(outputArr);
  
  //Defining width pattern to all cels
  let celsToWidth = $(".subhead-table-cel, .table-cel").not("#entries-col *");

  let maxHeight = 0;
  let maxWidth = 54;
  celsToWidth.each(function() {
    let elementWidth = $(this).outerWidth();
    if (elementWidth > maxWidth) {
        maxWidth = elementWidth;
    }
  });

  $(".table-cel").each(function() {
    let elementHeight = $(this).outerHeight();
    if (elementHeight > maxHeight) {
      maxHeight = elementHeight;
    }
  });
    
  celsToWidth.css("width", maxWidth + 5);
  $(".table-cel").css("height", maxHeight);
}

function insertInputsCelCol() {
  Object.keys(couplingSUT).forEach(key => {
    $(`#entries-col`).append(`<div class='table-cel ${key % 2 === 0 ? 'dark' : ''}'>` + key + "</div>");
  });
}

function insertOutputsSubHeadCelArray(arr) {
  let arrCels = "<div class='d-flex align-items-center'>";
  for (let i = 0; i < arr.length; i++) {
    arrCels += "<div class='subhead-table-cel w-100'>" + arr[i] + "</div>"
  }
  arrCels += '</div>';
  $(`#output-col`).append(arrCels);
}

function insertOutputsTableCelArray(outputs) {
  Object.entries(couplingSUT).forEach(entry => {
    let arrCels = "<div class='d-flex align-items-center'>";
    for (let i = 0; i < outputs.length; i++) {
      if(entry[1][outputs[i]] && entry[1][outputs[i]].length > 0) {
        arrCels += `<div class="table-cel coupled">` + entry[1][outputs[i]].map(testes => {
          return 'teste ' + testes[0] +' <=> ' + 'teste ' + testes[1];
        }).join('<br>') + "</div>";
      } else {
        arrCels += `<div class="table-cel justify-content-center ${entry[0] % 2 === 0 ? 'dark' : ''}"> X </div>`;
      }
    }
    arrCels += '</div>';
    $(`#output-col`).append(arrCels);
  });
}