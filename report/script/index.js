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
mountComponentList();
mountTestComparationTable();

function compareValues (a, b) {
  const isIntegerA = parseInt(a) === a
  const isIntegerB = parseInt(b) === b
  if (isIntegerA !== isIntegerB) {
    return false;
  } else if (isIntegerA) {
    return a === b;
  } else {
    // Floating point numbers should have 10^-5 precision
    return Math.abs(a - b) < 1e-5;
  }
}

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


function mountComponentList(componentsArr = components) {
  componentsArr.forEach((component, index) => {
    if(Object.keys(component['couplings']).length !== 0) {
      $('#components-list').append(`<a href='coupling_component_detail.html?component=${index}'>` + component.name + "</a>");
    }
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
  insertTableCol(inputs, 'inputs', 'entries-col');
  compareAndInsertCelArray()
}

function insertTableCel(el_id, text, isDark) {
  $(`#${el_id}`).append(`<div class='table-cel ${isDark ? 'dark' : ''}'>` + text + "</div>");
}

function compareAndInsertCelArray() {
  const testErrors = []
  for (let i = 0; i < tests.length; i++) {
    const test = tests[i];
    testErrors.push([])
    for (let j = 0; j < test.outputs.length; j++) {
      const expectedOutput = test.expected_outputs[j];
      const actualOutput = test.outputs[j];
      if(!compareValues(expectedOutput, actualOutput)) {
        testErrors[i].push(j)
      }
    }
  }
  insertTableCol(outputs, 'expected_outputs', 'expected-output-col', testErrors);
  insertTableCol(outputs, 'outputs', 'output-col', testErrors);
  insertResultCol(testErrors.map(errorEntry => errorEntry.length ? 'FAIL' : 'PASS'));
}

function insertTableCol(subhead_arr, fieldName, el_id, testErrors=null) {
  for (let testColumn = 0; testColumn < subhead_arr.length; testColumn++) {
    let arrCels = "<div class='d-flex flex-column align-items-center w-100'>";
    const subhead = subhead_arr[testColumn];
    arrCels += "<div class='subhead-table-cel w-100'>" + subhead + "</div>"
    for (let testLine = 0; testLine < tests.length; testLine++) {
      const cel = tests[testLine][fieldName][testColumn];
      const hasError = testErrors?.[testLine].indexOf(testColumn) !== -1;
      arrCels += `<div class="table-cel text-wrap w-100 ${hasError ? 'error' : ''} ${testLine % 2 === 0 ? 'dark' : ''}" >` + cel + "</div>"
    }
    arrCels += '</div>';
    $(`#${el_id} .cels-spot`).append(arrCels);
  }
}


function insertResultCol(result_arr) {
  let arrCels = "<div class='d-flex flex-column align-items-center w-100'>";
  result_arr.forEach(result => {
    arrCels += `<div class="table-cel text-wrap w-100 ${result === 'FAIL' ? 'error' : 'success'}" >` + result + "</div>"
  });
  $(`#results-col .cels-spot`).append(arrCels);
}