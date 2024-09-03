# Revisão

## DCCC analysis

---------------

### Componentes

Para entendermos do que se trata **DC(*Data Coupling*)** e **CC(*Control Coupling*)** e como , antes é preciso compreender o conceito de componente em um software. Os componentes de um sistema devem derivar, ou abranger, uma arquitetura de software e requisitos de baixo-nivel(*low-level*). Não necessáriamente cada implementação de um requisito de baixo nível resulta em um componente do sistema, o que é importante saber é que trata-se de uma abstração para partes do código que, quando executado, seu resultado contribuirá para a execução de uma funcionalidade do sistema.Para sistemas orientados a objeto, componentes são os métodos de uma classe.

Então, a componetização de uma funcionalidade está na divisão de um bloco grande de código, que representa uma determinada funcionalidade do software(que contém um requisito atrelado), em outros pequenos blocos, que por sua vez, quando executados, compõem uma parecela de importância para aquela funcionalidade. Essas divisões, chamadas de componentes, ajudam no momento dos testes do software para melhor identificação de erros quando há ocorrência de falta.

#### Componentes integrados

Componentes integrados são componentes que, de alguma forma dependem ou são dependências de outros componentes, esses casos são chamados de *coupling*(acoplamento).

### Verificação de acoplamento

Com o conceito de compomente já apresentado, podemos adentrar na verificação dos acoplamentos entre componentes em um software. A análise de **DCCC** ajuda na demonstração de interações entre componentes, sejam elas intencionais, ou não. Para que uma cobertura de DCCC seja feita de forma mais precisa, os testes baseados em requisitos precisam fazer parte da analise.

#### DC(*Data Coupling*)

*Data Coupling* é o caso de acoplamento entre componentes via dependência de um dado. Ou seja, um componente X, que depende de um dado proveniente de um componente Y, contempla um caso de *data coupling*

#### CC(*Control Coupling*)

*Control Coupling* é o caso de acoplamento na qual um componente sofre alterações no seu fluxo de controle por conta da execução de outro componente. Ou seja, se um componente X, para que seja executado de forma a ter o comportamento correto e esperado, precisa necessáriamente ser executado antes do componente Y, isso o classificaria como um acoplamento de controle.
