# Revisão

## DCCC analysis

### Componentes

Para entendermos do que se trata **DC(*Data Coupling*)** e **CC(*Control Coupling*)** e como , antes é preciso compreender o conceito de componente em um software. Os componentes de um sistema devem derivar, ou abranger, uma arquitetura de software e requisitos de baixo-nivel(*low-level*). Não necessáriamente cada implementação de um requisito de baixo nível resulta em um componente do sistema, o que é importante saber é que trata-se de uma abstração para partes do código que, quando executado, seu resultado contribuirá para a execução de uma funcionalidade do sistema.Para sistemas orientados a objeto, componentes são os métodos de uma classe.

Então, a componetização de uma funcionalidade está na divisão de um bloco grande de código, que representa uma determinada funcionalidade do software(que contém um requisito atrelado), em outros pequenos blocos, que por sua vez, quando executados, compõem uma parecela de importância para aquela funcionalidade. Essas divisões, chamadas de componentes, ajudam no momento dos testes do software para melhor identificação de erros quando há ocorrência de falta.

#### Componentes integrados

Componentes integrados são componentes que, de alguma forma dependem ou são dependências de outros componentes, esses casos são chamados de *coupling*(acoplamento).

---------------

### Verificação de acoplamento

Com o conceito de compomente já apresentado, podemos adentrar na verificação dos acoplamentos entre componentes em um software. A análise de **DCCC** ajuda na demonstração de interações entre componentes, sejam elas intencionais, ou não. Para que uma cobertura de DCCC seja feita de forma mais precisa, os testes baseados em requisitos precisam fazer parte da analise.
Considerações sobre DCCC na DO-178C:

- A cobertura de de testes da estrutura do software(feita pelo DCCC) precisa ser alcançada para softwares DAL A/B/C.
- A análise deve confirmar a presença de acoplamentos entre os componentes.
- É requerido que os testes baseados em requisitos exercitem os acoplamentos.
- A análise de cobertura deve apontar interfaces que não foram exercitadas durante os testes, ou seja, deficiências em casos de teste baseado em requisitos, inadequações de requisitos de software, código estranho(incluíndo código morto e desativado).
- A intenção por trás da análise é garantir a suficiência dos testes.

Sem mais segredos, podemos finalmente classificar do que se trata os acoplamentos citados, e como eles são classificados.

#### DC(*Data Coupling*)

*Data Coupling* é o caso de acoplamento entre componentes via dependência de um dado. Ou seja, um componente X, que depende de um dado proveniente de um componente Y, contempla um caso de *data coupling*

#### CC(*Control Coupling*)

*Control Coupling* é o caso de acoplamento na qual um componente sofre alterações no seu fluxo de controle por conta da execução de outro componente. Ou seja, se um componente X, para que seja executado de forma a ter o comportamento correto e esperado, precisa necessáriamente ser executado antes do componente Y, isso o classificaria como um acoplamento de controle.

#### Exemplo

  Esse é um exemplo simples de códigos que mostra a relação de acoplamento entre componentes. Neste exemplo os componentes são as funções contidas nos arquivos(sensor.cpp e airspeed.cpp), os códigos simulam de maneira bem simplória leitura de sensores de pressão e como isso influencia na velocidade da aeronave.
  
  ``` cpp
  sensors.cpp
  
  void sensors::update_static_pressure(void) {
    //code...
    if (delta_SP12 <= STATIC_PREASSURE_ALLOED_ERROR) {
      global_static_pressure = SP1;
    } else if (delta_SP23 <= STATIC_PREASSURE_ALLOED_ERROR) {
      global_static_pressure = SP3;
    } else if (delta_SP13 <= STATIC_PREASSURE_ALLOED_ERROR) {
      global_static_pressure = SP2;
    } else {
      register_error(STATIC_PRESSURE_READ_ERROR);
      airspeed::disable_static_pressure_sensor();
    }
    //code ...
  }
  ```

   ``` cpp
  airspeed.cpp
  
  void airspeed::disable_static_pressure_sensor(void) {
    SP_mode = ESTIMATED;
  }
  
  float airspeed::compute_indicated_airspeed(void) {
    //code...
    switch(SP_mode) {
      case SENSORS:
        SP = global_static_pressure;
        break;
      
      case ESTIMATED:
        SP = get_static_pressure_estimate();
        break;
    }
    //code...
  }
  ```

É possível identificar os dois tipos de acoplamentos nesse exemplo. Perceba que existem relações de *data coupling* entre o componente `update_static_pressure(void)` e o `compute_indicated_airspeed(void)`, pois a váriavel `global_static_pressure` que é usada no componente presente em `airspeed.cpp` pode ter seu valor definido nas condicionais presentes em `sensors.cpp`.

Além disso, através desse exemplo, também é possível inferir uma relação de *control coupling* entre  `update_static_pressure(void)` e `disable_static_pressure_sensor(void)`, já que o fluxo de controle de `update_static_pressure(void)` pode ser de certa forma "interrompido", para dar vez a execução do componente do `airspeed.cpp`.

---------------

### Ferramenta de DCCC

---------------

## Referências

  [Hui Hua et al 2021 J. Phys.: Conf. Ser. 1827 012098](https://iopscience.iop.org/article/10.1088/1742-6596/1827/1/012098/pdf)
  <https://www.rapitasystems.com/blog/control-coupling-basics-do-178c>
  <https://www.faa.gov/sites/faa.gov/files/aircraft/air_cert/design_approvals/air_software/AR-07-19.pdf>