import os
import json
import webbrowser

class Component:
    def __init__(self, name, couplings={}):
        self.name = name
        self.couplings = couplings

    def add_coupling(self, name, sut_outputs=None, forced=False):
        if sut_outputs is None:
            sut_outputs = []
        self.couplings[name] = {"sut_outputs": sut_outputs, "forced": forced}
    
    def to_dict(self):
        return {
            "name": self.name,
            "couplings": self.couplings
        }
    

def report_results_in_js (test_results, analysis_results, analysis_results_tricked):
    coupling_SUT = serializable_analysis(analysis_results.input_params)
    components = init_components(analysis_results.internal_vars, test_results.functions_defs)
    components = incriese_components(components, analysis_results_tricked)
    tests = serialize_tests(test_results)

    report = {
        "coupling_SUT": coupling_SUT,
        "test_results": tests,
        "components": components
        }
    report = json.dumps(report)
    report_js = "const json_data = " + report

    report_js_path = os.path.abspath("./report/reporter.js")
    with open(report_js_path, "w") as file:
        file.write(report_js)
        file.close()
    print('Relatório de cobertura da análise de DC/CC montado, acesso o relatório em report/index.html')
    index_html_path = os.path.abspath("./report/index.html")
    webbrowser.open_new(index_html_path)


def init_components(internal_values, functions):
    components = []

    for func_name, func_params in functions.items():
        couplings = {}
        for param in func_params:
            if param.get("local"):
                internal_name = param["call_name"]
                if internal_name in internal_values:
                    sut_outputs = internal_values[internal_name].get("sut_outputs", [])
                    forced = str(internal_values[internal_name]["status"]) != "AnalysisStatus.SUCCESS"
                    couplings[internal_name] = {
                        "sut_outputs": sut_outputs if sut_outputs else [],
                        "forced": forced
                    }

        component = Component(name=func_name, couplings=couplings)
        components.append(component.to_dict())
    return components


def incriese_components(components, forced_analysis):
    for component in components:
        for var_name in component['couplings']:
            component['couplings'][var_name]['sut_outputs'] = forced_analysis[var_name]['sut_outputs'] if forced_analysis[var_name]['sut_outputs'] else []
    return components


def serializable_analysis(coupling_SUT):
    for input in coupling_SUT:
        if(str(coupling_SUT[input]["status"]) == "AnalysisStatus.AMBIGUOUS"):
            coupling_SUT[input]['analysed'] = False
        else:
            coupling_SUT[input]['analysed'] = True
        del(coupling_SUT[input]["status"])

    return coupling_SUT

def serialize_tests(test_results):
    tests = test_results[:len(test_results)]
    for test in tests:
        test.expected_outputs.extend(test.outputs)
    for fail in test_results.failed_tests:
        tests[fail.test_number].expected_outputs[fail.param_idx] = fail.expected_value
    return tests