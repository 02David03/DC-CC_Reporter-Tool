const json_data = {
  "warnings": [
    "Não foi possível avaliar acoplamento para as entradas 2, 3 e 4, por favor considere aumentar o vetor de testes",
    "Ao utilizar o valor 54 para a saída 'output' do componente <processInput> o sistema apresentou uma excessão"
  ],
  "coupling_SUT": {
    "1": {
      "0": [2, 7],
      "4": [7]
    },
    "2": {},
    "3": {},
    "4": {},
    "5": {
      "2": [4],
      "3": [5]
    },
    "6": {
      "5": [1, 4, 8]
    }
  },
  "test_results": {
    "0": {
      "timestamp": 1731536734,
      "inputs": [45, 46, 50, 1, 8, 9],
      "expected_outputs": [8, 1, 30, 0, 50],
      "obtained_outputs": [8, 1, 30, 0, 50]
    },
    "1": {
      "timestamp": 1731536735,
      "inputs": [44, 46, 50, 1, 8, 9], 
      "expected_outputs": [8, 1, 30, 0, 50],
      "obtained_outputs": [8, 1, 30, 0, 49]
    },
    "2": {
      "timestamp": 1731536736,
      "inputs": [45, 46, 50, 2, 8, 9],
      "expected_outputs": [8, 1, 30, 0, 50],
      "obtained_outputs": [8, 2, 30, 0, 50]
    },
    "3": {
      "timestamp": 1731536737,
      "inputs": [45, 46, 51, 1, 8, 9],
      "expected_outputs": [8, 1, 30, 0, 50],
      "obtained_outputs": [8, 1, 30, 1, 50]
    },
    "4": {
      "timestamp": 1731536738,
      "inputs": [45, 46, 50, 1, 7, 9], 
      "expected_outputs": [8, 1, 30, 0, 50],
      "obtained_outputs": [8, 1, 30, 0, 50]
    },
    "5": {
      "timestamp": 1731536739,
      "inputs": [45, 47, 50, 1, 8, 9],
      "expected_outputs": [8, 1, 30, 0, 50],
      "obtained_outputs": [8, 1, 30, 0, 51]
    },
    "6": {
      "timestamp": 1731536740,
      "inputs": [45, 46, 50, 1, 8, 10], 
      "expected_outputs": [8, 1, 30, 0, 50],
      "obtained_outputs": [7, 1, 30, 0, 50]
    },
    "7": {
      "timestamp": 1731536741,
      "inputs": [43, 46, 50, 1, 8, 9],
      "expected_outputs": [8, 1, 30, 0, 50],
      "obtained_outputs": [8, 1, 30, 0, 50]
    },
    "8": {
      "timestamp": 1731536742,
      "inputs": [45, 46, 52, 1, 8, 9],
      "expected_outputs": [8, 1, 30, 0, 50],
      "obtained_outputs": [8, 1, 29, 0, 50]
    }
  },
  "components": [
    {
      "name": "validateInput",
      "output_names": ["output", "validation"],
      "couplings": {
        "0": {
          "6": [4, 7],
          "4": [7],
          "5": [10]
        }
      }
    },
    {
      "name": "calculateResult",
      "output_names": ["result"],
      "couplings": {
        "0": {
          "2": [3, 1],
          "4": [2.5]
        }
      }
    },
    {
      "name": "analyzeData",
      "output_names": ["validation", "report"],
      "couplings": {
        "0": {
          "1": [3, 5],
          "3": [4]
        },
        "1": {
          "0": [2.5, 1],
          "4": [3]
        }
      }
    },
    {
      "name": "processInput",
      "output_names": ["output"],
      "couplings": {
        "0": {
          "1": [4, 3],
          "3": [2.5, 1]
        }
      }
    },
    {
      "name": "validateUser",
      "output_names": ["userValid", "errors"],
      "couplings": {
        "0": {
          "3": [1],
          "4": [2, 3]
        },
        "1": {
          "0": [1.5],
          "2": [4, 2]
        }
      }
    },
    {
      "name": "filterInformation",
      "output_names": ["filteredData"],
      "couplings": {
        "0": {
          "2": [4.2],
          "3": [1, 3]
        }
      }
    },
    {
      "name": "generateSummary",
      "output_names": ["summary", "status"],
      "couplings": {
        "0": {
          "2": [3, 2.5],
          "3": [1]
        },
        "1": {
          "0": [4, 5],
          "1": [3]
        }
      }
    },
    {
      "name": "calculateAverage",
      "output_names": ["averageCalculated", "standardDeviation"],
      "couplings": {
        "0": {
          "3": [3, 1],
          "4": [2.5]
        },
        "1": {
          "0": [4],
          "1": [2, 1.5]
        }
      }
    },
    {
      "name": "checkCondition",
      "output_names": ["statusChecked"],
      "couplings": {
        "0": {
          "1": [2, 3.5],
          "4": [1]
        }
      }
    }
  ]
}