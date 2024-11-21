const components = json_data.components;
const tests = json_data.test_results;
const couplingSUT = json_data.coupling_SUT;

let componentIndex = 0;
let selectedComponent = {};
let outputs = []
let vars = []

getComponentIndex();
setVarsAndOutputs();
changeSelectedComponent();

function getComponentIndex() {
  const urlParams = new URLSearchParams(window.location.search);
  componentIndex = urlParams.get('component') ?? 0;
}

function changeSelectedComponent(index = componentIndex) {
  selectedComponent = components[index];
  mountComponentDetail()
}

function mountComponentDetail() {
  insertComponentName();
  mountAnalysesGRN1();
  setComponentListHeight();
  mountComponentList();
  mountComponentTable();
}

function mountAnalysesGRN1() {
  let graphData = [0, 0]; 
  for(const key in selectedComponent['couplings']) {
    const sutOutputs = selectedComponent['couplings'][key]['sut_outputs'];
    const hasCouplings = sutOutputs.length > 0; 
    if(hasCouplings) {
      graphData[0]++
    } else{
      graphData[1]++
    }
  }

  mountCouplingGridGraph("GRN1-grid-graph", "GRN1-tooltip", selectedComponent['couplings'], true);
  mountCouplingDonutGraph("GRN1-donut-graph", "GRN1-tooltip", graphData, true);
}

function mountComponentList(componentsArr = components) {
  $('#components-list').children().remove();
  componentsArr.forEach((component, index) => {
    $('#components-list').append(`<span class='fake-link' onclick='changeSelectedComponent(${index})'>` + component.name + "</span>");
  });
}

function setVarsAndOutputs() {
  outputs = Object.keys(Object.values(couplingSUT)[0]).filter(name => name !== 'analysed');
  vars = Object.keys(tests[0][3]);
}

$(document).on('input', '#component-filter', function() {
  let value = $(this).val();
  let filteredComponents = components.filter(component => component.name.includes(value));
  mountComponentList(filteredComponents);
});

function setComponentListHeight() {
  $('#components-col').css("height", $('#GRN1-col').css("height"));
}

function insertComponentName() {
  $('.add-component-name').each( function() {
    let text = $(this).text();
    let splitedText = text.split('componente');
    $(this).text(splitedText[0] + `componente ${selectedComponent.name}`)
  });
}

function mountComponentTable() {
  console.log(tests)
  for (let i = 0; i < tests.length; i++) {
    insertTableCel('test-col', `Teste ${i + 1}`, (i % 2 === 0));
  }
  insertTableCol(vars, 3, 'comp-vars-col', true);
  insertTableCol(outputs, 1, 'sut-outputs-col');
}

function insertTableCel(el_id, text, isDark) {
  $(`#${el_id}`).append(`<div class='table-cel ${isDark ? 'dark' : ''}'>` + text + "</div>");
}

function insertTableCol(subhead_arr, index, el_id, is_obj = false) {
  for (let i = 0; i < subhead_arr.length; i++) {
    let arrCels = "<div class='d-flex flex-column align-items-center w-100'>";
    const subhead = subhead_arr[i];
    arrCels += "<div class='subhead-table-cel w-100'>" + subhead + "</div>"
    for (let j = 0; j < tests.length; j++) {
      let cel = is_obj ? tests[j][index][subhead_arr[i]] : tests[j][index][i];
      arrCels += `<div class="table-cel text-wrap w-100 ${j % 2 === 0 ? 'dark' : ''}" >` + cel + "</div>"
    }
    arrCels += '</div>';
    $(`#${el_id} .cels-spot`).append(arrCels);
  }
}
