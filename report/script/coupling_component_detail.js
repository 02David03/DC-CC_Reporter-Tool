const components = json_data.components
let componentIndex = 0;
let selectedComponent = {};

getComponentIndex();
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
    const subObj = selectedComponent['couplings'][key];
    const hasValues = Object.keys(subObj).some(
      subKey => subObj[subKey].length > 0
    );
    if(hasValues) {
      graphData[0]++
    } else{
      graphData[1]++
    }
  }

  mountCouplingGridGraph("GRN1-grid-graph", "GRN1-tooltip", selectedComponent['couplings'], true);
  mountCouplingDonutGraph("GRN1-donut-graph", "GRN1-tooltip", graphData);
}

function mountComponentList(componentsArr = components) {
  $('#components-list').children().remove();
  componentsArr.forEach((component, index) => {
    $('#components-list').append(`<span class='fake-link' onclick='changeSelectedComponent(${index})'>` + component.name + "</span>");
  });
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
  $('#comp-outputs-col').children().not(".head-table-cel, .subhead-table-cel").remove();
  $('#sut-outputs-col').children().not(".head-table-cel").remove();
  insertComponentOutputsCel();
  let outputArr = [];
  Object.values(selectedComponent['couplings']).forEach(value => {
    outputArr = [...new Set([...(Object.keys(value)), ...outputArr])];
  });
  outputArr = outputArr.sort();
  insertOutputsSubHeadCel(outputArr);
  insertOutputsTableCelArray(outputArr);

  let cels = $(".subhead-table-cel, .table-cel").not("#comp-outputs-col *");
  let maxWidth = 54;
  cels.each(function() {
      let elementWidth = $(this).outerWidth();
      if (elementWidth > maxWidth) {
          maxWidth = elementWidth;
      }
    });

    cels.css("width", maxWidth);
}

function insertComponentOutputsCel() {
  let arrCels = "<div class='d-flex flex-column align-items-center'>";
  for (let i = 0; i < selectedComponent.output_names.length; i++) {
    arrCels += `<div class='table-cel w-100 ${i % 2 === 0 ? 'dark' : ''}'>` + selectedComponent.output_names[i] + "</div>"
  }
  arrCels += '</div>';
  $(`#comp-outputs-col`).append(arrCels);
}

function insertOutputsSubHeadCel(arr) {
  let arrCels = "<div class='d-flex align-items-center'>";
  for (let i = 0; i < arr.length; i++) {
    arrCels += "<div class='subhead-table-cel w-100'>#" + arr[i] + "</div>"
  }
  arrCels += '</div>';
  $(`#sut-outputs-col`).append(arrCels);
}

function insertOutputsTableCelArray(outputs) {
  Object.entries(selectedComponent['couplings']).forEach(entry => {
    let arrCels = "<div class='d-flex align-items-center'>";
    for (let i = 0; i < outputs.length; i++) {
      if(entry[1][outputs[i]]) {
        arrCels += `<div class="table-cel coupled">` + entry[1][outputs[i]] + "</div>";
      } else {
        arrCels += `<div class="table-cel ${entry[0] % 2 === 0 ? 'dark' : ''}"> # </div>`;
      }
    }
    arrCels += '</div>';
    $(`#sut-outputs-col`).append(arrCels);
  });
}