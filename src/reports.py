import os
import json
import webbrowser

from dc_cc_analyzer import AnalysisStatus
    

def report_results_in_js (components_defs, test_results, analysis_results, analysis_results_tricked):
    coupling_SUT = _serialize_inputs_analysis(analysis_results.input_params)
    components = _init_components(analysis_results.internal_vars, components_defs, analysis_results_tricked)

    report = {
        'coupling_SUT': coupling_SUT,
        'test_results': list(map(lambda test: test._asdict(), test_results[:])),
        'components': components
    }
    report = json.dumps(report)
    report_js = 'const json_data = ' + report

    report_js_path = os.path.abspath('./report/reporter.js')
    with open(report_js_path, 'w') as file:
        file.write(report_js)
        file.close()
    print('Relatório de cobertura da análise de DC/CC montado, acesso o relatório em report/index.html')
    index_html_path = os.path.abspath('./report/index.html')
    webbrowser.open_new(index_html_path)


def _init_components (internal_vars, components_defs, forced_analysis):
    components = []

    for func_name, func_params in components_defs.items():
        couplings = {}
        for param in func_params:
            passed_var_name = param['call_name']
            if passed_var_name in internal_vars:
                sut_outputs = forced_analysis[passed_var_name]['sut_outputs']
                forced = internal_vars[passed_var_name]['status'] == AnalysisStatus.AMBIGUOUS
                couplings[passed_var_name] = {
                    'sut_outputs': sut_outputs,
                    'forced': forced
                }

        components.append({
            'name': func_name,
            'couplings': couplings
        })
    return components


def _serialize_inputs_analysis (input_params):
    for param in input_params.values():
        param['analysed'] = param['status'] != AnalysisStatus.AMBIGUOUS
        del(param['status'])

    return input_params
