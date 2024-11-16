//Global variables
const warnings = json_data.warnings;
const couplingSUT = json_data.coupling_SUT;
const components = json_data.components;
const tests = json_data.test_results;
let componentSelected = 0;

//Call mount functions
mountWarningList();
mountAnalysesGRN0();
setComponentListHeight()
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

function setComponentListHeight() {
  $('#components-col').css("height", $('#GRN0-col').css("height"));
}

function mountComponentList(componentsArr = components) {
  $('#components-list').children().remove();
  componentsArr.forEach((component, index) => {
    $('#components-list').append(`<a href='coupling_component_detail.html?component=${index}'>` + component.name + "</a>");
  });
}

function selectComponent(index) {
  componentSelected = index;
}

$(document).on('input', '#component-filter', function() {
  let value = $(this).val();
  let filteredComponents = components.filter(component => component.name.includes(value));
  mountComponentList(filteredComponents);
});


function mountTestComparationTable() {
  //Add Subheaders
  let valueReference = Object.values(tests)[0];
  insertSubHeadCelArray('entries-col', valueReference.inputs.length);
  insertSubHeadCelArray('expected-output-col', valueReference.expected_outputs.length);
  insertSubHeadCelArray('output-col', valueReference.obtained_outputs.length);

  //Add cels
  Object.entries(tests).forEach(entry => {
    insertTableCel('test-col', `Teste ${entry[0]}`, (entry[0] % 2 === 0));
    insertTableCelArray('entries-col', entry[1].inputs, (entry[0] % 2 === 0));
    compareAndInsertCelArray( entry[1].expected_outputs, entry[1].obtained_outputs, (entry[0] % 2 === 0))
  });

  //Defining width pattern to all cels
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

function insertTableCel(el_id, text, isDark) {
  $(`#${el_id}`).append(`<div class='table-cel ${isDark ? 'dark' : ''}'>` + text + "</div>");
}

function insertSubHeadCelArray(el_id, range) {
  let arrCels = "<div class='d-flex align-items-center'>";
  for (let i = 0; i < range; i++) {
    arrCels += "<div class='subhead-table-cel w-100'> #" + (i + 1) + "</div>"
  }
  arrCels += '</div>';
  $(`#${el_id}`).append(arrCels);
}

function compareAndInsertCelArray(expected_outputs, obtained_outputs, isDark) {
  for (let i = 0; i < obtained_outputs.length; i++) {
    if(expected_outputs[i] !== obtained_outputs[i]) {
      obtained_outputs[i] += ' error';
    }
  }
  insertTableCelArray('expected-output-col', expected_outputs, isDark);
  insertTableCelArray('output-col', obtained_outputs, isDark);

}

function insertTableCelArray(el_id, arr, isDark) {
  let arrCels = "<div class='d-flex align-items-center'>";
  for (let i = 0; i < arr.length; i++) {
    hasError = String(arr[i]).includes('error');
    if(hasError) {
      arr[i] = arr[i].replace('error', '');
    }
    arrCels += `<div class="table-cel ${hasError ? 'error' : ''} ${isDark ? 'dark' : ''}">` + arr[i] + "</div>"
  }
  arrCels += '</div>';
  $(`#${el_id}`).append(arrCels);
}