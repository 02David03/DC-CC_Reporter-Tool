//Global variables
const warnings = json_data.warnings;
const couplingSUT = json_data.coupling_SUT;
const components = json_data.components;
const tests = json_data.test_results;

let inputs = []
let outputs = []

//Call mount functions
mountWarningList();
mountAnalysesGRN0();
setInputsAndOutputs();
setComponentListHeight()
mountComponentList();
mountTestComparationTable();

function mountWarningList() {
  if(!warnings) {
    $('#accordionWarning').addClass('d-none');
  } else {
    for (let i = 0; i < warnings.length; i++) {
      $('#warning-list').append("<li>" + warnings[i] + "</li>");
    }
  }
}

function mountAnalysesGRN0() {
  let graphData = [0, 0, 0];
  for(const key in couplingSUT) {
    const subObj = couplingSUT[key];
    if(!subObj['analysed']) {
      graphData[1]++
    } else {
      let hasAnyValue = false;
      Object.entries(subObj).forEach(entry => {
        if(entry[0] !== "analysed" && entry[1] !== null) hasAnyValue = true;
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

function setInputsAndOutputs() {
  Object.keys(couplingSUT).forEach((key, idx) => {
    inputs.push(key);
    if (idx === 0) {
      outputs.push(...Object.keys(couplingSUT[key]).filter(name => name !== 'analysed'));
    }
  });
}

function setComponentListHeight() {
  $('#components-col').css("height", $('#GRN0-col').css("height"));
}

function mountComponentList(componentsArr = components) {
  $('#components-list').children().remove();
  componentsArr.forEach((component, index) => {
    $('#components-list').append(`<a href='coupling_component_detail.html?component=${index}'>` + component.name + "</a>");
  });
}

$(document).on('input', '#component-filter', function() {
  let value = $(this).val();
  let filteredComponents = components.filter(component => component.name.includes(value));
  mountComponentList(filteredComponents);
});

function mountTestComparationTable() {
  for (let i = 0; i < tests.length; i++) {
    insertTableCel('test-col', `Teste ${i + 1}`, (i % 2 === 0));
  }
  insertTableCol(inputs, 0, 'entries-col');
  compareAndInsertCelArray()
}

function insertTableCel(el_id, text, isDark) {
  $(`#${el_id}`).append(`<div class='table-cel ${isDark ? 'dark' : ''}'>` + text + "</div>");
}

function compareAndInsertCelArray() {
  for (let i = 0; i < tests.length; i++) {
    const test = tests[i];
    for (let j = 0; j < test[1].length; j++) {
      let expected_output = test[2][j];
      let output = test[1][j];
      if(expected_output !== output) {
        test[2][j] +=' error';
        test[1][j] +=' error';
      }
    }
  }
  insertTableCol(outputs, 2, 'expected-output-col');
  insertTableCol(outputs, 1, 'output-col');
}

function insertTableCol(subhead_arr, index, el_id) {
  for (let i = 0; i < subhead_arr.length; i++) {
    let arrCels = "<div class='d-flex flex-column align-items-center w-100'>";
    const subhead = subhead_arr[i];
    arrCels += "<div class='subhead-table-cel w-100'>" + subhead + "</div>"
    for (let j = 0; j < tests.length; j++) {
      let cel = tests[j][index][i];
      let hasError = String(cel).includes('error');
      if(hasError) {
        cel = cel.replace('error', '');
      }
      arrCels += `<div class="table-cel text-wrap w-100 ${hasError ? 'error' : ''} ${j % 2 === 0 ? 'dark' : ''}" >` + cel + "</div>"
    }
    arrCels += '</div>';
    $(`#${el_id} .cels-spot`).append(arrCels);
  }
}
