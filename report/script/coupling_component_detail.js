const components = json_data.components;
const tests = json_data.test_results;
const couplingSUT = json_data.coupling_SUT;

let componentIndex = 0;
let selectedComponent = {};
let outputs = []
let vars = []

getComponentIndex();
setVarsAndOutputs();
mountComponentTable();
mountAnalysesTable();
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
  mountComponentList();
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
    if(Object.keys(component['couplings']).length !== 0) {
      $('#components-list').append(`<span class='fake-link' onclick='changeSelectedComponent(${index})'>` + component.name + "</span>");
    }
  });
}

function setVarsAndOutputs() {
  outputs = Object.keys(Object.values(couplingSUT)[0]).filter(name => name !== 'analysed');
  vars = Object.keys(tests[0].internal_vars);
}

$(document).on('input', '#component-filter', function() {
  let value = $(this).val();
  let filteredComponents = components.filter(component => component.name.includes(value));
  mountComponentList(filteredComponents);
});

function insertComponentName() {
  $('.add-component-name').each( function() {
    let text = $(this).text();
    let splitedText = text.split('componente');
    $(this).text(splitedText[0] + `componente ${selectedComponent.name}`)
  });
}

function mountComponentTable() {
  for (let i = 0; i < tests.length; i++) {
    insertTableCel('test-col', `Teste ${i + 1}`, (i % 2 === 0));
  }
  insertTableCol(vars, 'internal_vars', 'comp-vars-col', true);
  insertTableCol(outputs, 'outputs', 'sut-outputs-col');
}

function mountAnalysesTable() {
  for (let i = 0; i < outputs.length; i++) {
    insertTableCel('sut-outputs-col-2', `${outputs[i]}`, (i % 2 === 0));
  }
  let coupled_vars = vars.reduce((a, v) => ({ ...a, [v]: {sut_outputs: [], forced: false}}), {})
  components.forEach(component => {
    Object.entries(component['couplings']).forEach(entry => {
      let concat_arr = coupled_vars[entry[0]]['sut_outputs'].concat(entry[1]['sut_outputs']);
      let set = new Set(concat_arr);
      coupled_vars[entry[0]]['sut_outputs'] = Array.from(set);
      coupled_vars[entry[0]]['forced'] = entry[1]['forced']
    });
  });

  console.log(coupled_vars)
  insertVarsCol(coupled_vars);
}

function insertTableCel(el_id, text, isDark) {
  $(`#${el_id}`).append(`<div class='table-cel ${isDark ? 'dark' : ''}'>` + text + "</div>");
}

function insertTableCol(subhead_arr, fieldName, el_id, is_obj = false) {
  for (let i = 0; i < subhead_arr.length; i++) {
    let arrCels = "<div class='d-flex flex-column align-items-center w-100'>";
    const subhead = subhead_arr[i];
    arrCels += "<div class='subhead-table-cel w-100'>" + subhead + "</div>"
    for (let j = 0; j < tests.length; j++) {
      let cel = is_obj ? tests[j][fieldName][subhead_arr[i]] : tests[j][fieldName][i];
      arrCels += `<div class="table-cel text-wrap w-100 ${j % 2 === 0 ? 'dark' : ''}" >` + cel + "</div>"
    }
    arrCels += '</div>';
    $(`#${el_id} .cels-spot`).append(arrCels);
  }
}

function insertVarsCol(coupled_vars) {
  Object.entries(coupled_vars).forEach(entry => {
    
    let arrCels = "<div class='d-flex flex-column align-items-center w-100'>";
    arrCels += "<div class='subhead-table-cel w-100'>" + entry[0] + "</div>"
    arrCels += `<div class='table-cel dark ${entry[1].forced ? 'error': 'opacity-0'} w-100'>` + 'Forced' + "</div>"
    
    outputs.forEach((output, i) => {
      let coupled = entry[1].sut_outputs.includes(output);
      arrCels += `<div class="table-cel text-wrap w-100 ${i % 2 === 0 ? 'dark' : ''} ${coupled ? 'coupled' : ''}">` + (coupled ? 'O' : 'X') + "</div>"
    });

    arrCels += '</div>';
    $(`#comp-vars-col-2 .cels-spot`).append(arrCels);
  });
}

