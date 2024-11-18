const couplingSUT = json_data.coupling_SUT;

mountAnalysesGRN0();
mountInputsTable();

function mountAnalysesGRN0() {
  let graphData = [0, 0];
  for(const key in couplingSUT) {
    const subObj = couplingSUT[key];
    const hasValues = Object.keys(subObj).some(
      subKey => subObj[subKey].length > 0
    );
    if(hasValues) {
      graphData[0]++
    } else{
      graphData[1]++
    }
  }
  mountCouplingDonutGraph("GRN0-donut-graph", "GRN0-tooltip", graphData);
  mountCouplingGridGraph("GRN0-grid-graph", "GRN0-info-box", couplingSUT);
}


function mountInputsTable() {
  insertInputsCelCol();
  let outputArr = [];
  Object.values(couplingSUT).forEach(value => {
    outputArr = [...new Set([...(Object.keys(value)), ...outputArr])];
  });
  outputArr = outputArr.sort();
  insertOutputsSubHeadCelArray(outputArr);
  insertOutputsTableCelArray(outputArr);
  
  //Defining width pattern to all cels
  let cels = $(".subhead-table-cel, .table-cel").not("#entries-col *");

  let maxWidth = 54;
  cels.each(function() {
      let elementWidth = $(this).outerWidth();
      if (elementWidth > maxWidth) {
          maxWidth = elementWidth;
      }
    });

    cels.css("width", maxWidth);
}

function insertInputsCelCol() {
  Object.keys(couplingSUT).forEach(key => {
    $(`#entries-col`).append(`<div class='table-cel ${key % 2 === 0 ? 'dark' : ''}'>#` + key + "</div>");
  });
}

function insertOutputsSubHeadCelArray(arr) {
  let arrCels = "<div class='d-flex align-items-center'>";
  for (let i = 0; i < arr.length; i++) {
    arrCels += "<div class='subhead-table-cel w-100'> #" + arr[i] + "</div>"
  }
  arrCels += '</div>';
  $(`#output-col`).append(arrCels);
}

function insertOutputsTableCelArray(outputs) {
  Object.entries(couplingSUT).forEach(entry => {
    let arrCels = "<div class='d-flex align-items-center'>";
    for (let i = 0; i < outputs.length; i++) {
      if(entry[1][outputs[i]]) {
        arrCels += `<div class="table-cel coupled">` + entry[1][outputs[i]] + "</div>";
      } else {
        arrCels += `<div class="table-cel ${entry[0] % 2 === 0 ? 'dark' : ''}"> # </div>`;
      }
    }
    arrCels += '</div>';
    $(`#output-col`).append(arrCels);
  });
}