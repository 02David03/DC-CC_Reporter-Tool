const json_data = {
  "warnings": [
    "Ao utilizar o valor 54 para a saída 'output' do componente <processInput> o sistema apresentou uma excessão"
  ],
  "coupling_SUT": {
    "i1": {
      "o1": [[1,5], [2,6]],
      "o4": [[2,4]],
      analysed: true
    },
    "i2": {analysed: true},
    "i3": {analysed: false},
    "i4": {analysed: false},
    "i5": {
      "o5": [[4, 6]],
      analysed: true
    },
    "i6": {
      "o3": [[1, 4]],
      analysed: true
    }
  },
  "test_results": {
    "1": {
      "inputs": [44.5, 46.2, 50, 1, 8.1, 9],
      "expected_outputs": [8, 1, 30, 0, 50.3],
      "obtained_outputs": [8, 1, 30, 0, 49.9]
    },
    "2": {
      "inputs": [45, 46, 50.5, 2, 8, 9.7],
      "expected_outputs": [8, 1.5, 30, 0, 50],
      "obtained_outputs": [8, 1.7, 30, 0, 50]
    },
    "3": {
      "inputs": [45, 46.1, 51, 1, 8, 9.3],
      "expected_outputs": [8.2, 1, 30, 0, 50],
      "obtained_outputs": [8.2, 1, 30, 1, 50]
    },
    "4": {
      "inputs": [45, 46, 50, 1, 7.9, 9],
      "expected_outputs": [8, 1, 30, 0, 50],
      "obtained_outputs": [8, 1, 30, 0, 50]
    },
    "5": {
      "inputs": [45, 47.3, 50, 1, 8, 9],
      "expected_outputs": [8, 1, 30, 0.1, 50],
      "obtained_outputs": [8, 1, 30, 0.1, 51.2]
    },
    "6": {
      "inputs": [45, 46, 50, 1.2, 8, 10],
      "expected_outputs": [7.8, 1, 30, 0, 50.5],
      "obtained_outputs": [7.7, 1, 30, 0, 50.5]
    },
    "7": {
      "inputs": [43.9, 46, 50, 1, 8, 9],
      "expected_outputs": [8, 1, 30, 0, 50],
      "obtained_outputs": [8, 1, 30, 0, 50]
    },
    "8": {
      "inputs": [45, 46, 52, 1, 8, 9],
      "expected_outputs": [8, 1, 30, 0.3, 50],
      "obtained_outputs": [8, 1, 29.8, 0.3, 50]
    },
    "9": {
      "inputs": [45, 46, 52.7, 1, 8, 9],
      "expected_outputs": [8, 1, 30, 0, 50],
      "obtained_outputs": [8, 1, 29.9, 0, 50]
    },
    "10": {
      "inputs": [45.3, 46, 52, 1, 8, 9],
      "expected_outputs": [8, 1.2, 30, 0, 50],
      "obtained_outputs": [8, 1.2, 29.9, 0, 50]
    },
    "11": {
      "inputs": [45, 46, 52, 1, 8.4, 9.5],
      "expected_outputs": [8, 1, 30, 0, 50.1],
      "obtained_outputs": [8, 1, 29.9, 0, 50.1]
    }
  },
  "components": [
    {
      "name": "analyzeData",
      "couplings": {
        "validation": {sut_outputs: ['o2', 'o3'], forced: false},
        "report":{sut_outputs: [], forced: true},
      }
    },
    {
      "name": "makeMagic",
      "couplings": {
        "magic_numb": {sut_outputs: ['o3', 'o2'], forced: true},
        "transform_numb":{sut_outputs: ['o2', 'o4'], forced: true},
        "the_numb":{sut_outputs: ['o1'], forced: false},
        "no_numb":{sut_outputs: [], forced: true},
      }
    },
    {
      "name": "calcTotal",
      "couplings": {
        "result": {sut_outputs: ['o5'], forced: false},
      }
    },
    {
      "name": "partitionateTotal",
      "couplings": {
        "part_1": {sut_outputs: [], forced: true},
        "part_2": {sut_outputs: ['o2'], forced: true},
        "part_3": {sut_outputs: ['o3'], forced: true},
      }
    },
    {
      "name": "finishCount",
      "couplings": {
        "finish": {sut_outputs: [], forced: true},
      }
    },
    {
      "name": "initiateCount",
      "couplings": {
        "count": {sut_outputs: ['o2', 'o1', 'o6'], forced: false},
        "data_life": {sut_outputs: ['o6'], forced: true},
      }
    },
  ]
}