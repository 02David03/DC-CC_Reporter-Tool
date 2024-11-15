//Global variables
const warnings = json_data.warnings;
const couplingSUT = json_data.coupling_SUT;
const components = json_data.components;

//Call mount functions
mountWarningList();
mountAnalysesGRN0();

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
  mountDonutCouplingGraph("GRN0-index-graph", "GRN0-tooltip", graphData);

}