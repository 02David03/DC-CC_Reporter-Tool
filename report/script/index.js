//Global variables
const warnings = json_data.warnings;
const couplingSUT = json_data.coupling_SUT;
const components = json_data.components;
const tests = json_data.test_results;

//Call mount functions
mountWarningList();
mountAnalysesGRN0();
mountComponentList();
mountTestComparationTable();

function mountWarningList() {
  if(warnings.length === 0) {
    $('#warning-list').addClass('d-none');
  } else {
    for (let i = 0; i < warnings.length; i++) {
      $('#warning-list').append("<li>" + warnings[i] + "</li>");
    }
  }
}

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

function mountComponentList() {

}

function mountTestComparationTable() {
  //Add Subheaders
  let valueReference = Object.values(tests)[0];
  insertSubHeadCelArray('entries-col', valueReference.inputs.length);
  insertSubHeadCelArray('expected-output-col', valueReference.expected_outputs.length);
  insertSubHeadCelArray('output-col', valueReference.obtained_outputs.length);

  //Add cels
  Object.entries(tests).forEach(entry => {
    insertTableCel('test-col', `Teste ${entry[0]}`);
    insertTableCelArray('entries-col', entry[1].inputs);
    compareAndInsertCelArray( entry[1].expected_outputs, entry[1].obtained_outputs)
  });

  //Definindo tamanho padrão para todas as celulas
  let cels = $(".subhead-table-cel, .table-cel").not("#test-col *");

  let maxWidth = 54;
  cels.each(function() {
      let elementWidth = $(this).outerWidth();
      if (elementWidth > maxWidth) {
          maxWidth = elementWidth;
      }
    });

    cels.css("width", maxWidth);
}

function insertTableCel(el_id, text) {
  $(`#${el_id}`).append("<div class='table-cel'>" + text + "</div>");
}

function insertSubHeadCelArray(el_id, range) {
  let arrCels = "<div class='d-flex align-items-center'>";
  for (let i = 0; i < range; i++) {
    arrCels += "<div class='subhead-table-cel'> #" + (i + 1) + "</div>"
  }
  arrCels += '</div>';
  $(`#${el_id}`).append(arrCels);
}

function compareAndInsertCelArray(expected_outputs, obtained_outputs) {
  for (let i = 0; i < obtained_outputs.length; i++) {
    if(expected_outputs[i] !== obtained_outputs[i]) {
      obtained_outputs[i] += ' error';
    }
  }
  insertTableCelArray('expected-output-col', expected_outputs);
  insertTableCelArray('output-col', obtained_outputs);

}

function insertTableCelArray(el_id, arr) {
  let arrCels = "<div class='d-flex align-items-center'>";
  for (let i = 0; i < arr.length; i++) {
    hasError = String(arr[i]).includes('error');
    if(hasError) {
      arr[i] = arr[i].replace('error', '');
    }
    arrCels += `<div class="table-cel ${hasError ? 'error' : '' }">` + arr[i] + "</div>"
  }
  arrCels += '</div>';
  $(`#${el_id}`).append(arrCels);
}