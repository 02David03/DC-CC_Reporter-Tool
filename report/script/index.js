//Global variables
let warnings = [];
let couplingSUT = {};
let components = {};


init();

async function init() {
  await $.getJSON('reporter.json', function(data) {
    warnings = data.warnings;
    couplingSUT = data.couplingSUT;
    components = data.components;
  });

  mountWarningList();
}

function mountWarningList() {
  for (let i = 0; i < warnings.length; i++) {
    $('#warning-list').append("<li>" + warnings[i] + "</li>");
  }
}