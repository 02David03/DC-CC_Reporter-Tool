Revisão bibliográfica - Data Coupling and Control Coupling DC/CC - TCC

Objetivo do TCC: Desenvolver uma ferramenta, daqui em diante referenciada como Ferramenta, que execute um conjunto
de casos de testes e determine a cobertura DC/CC de um código.

Tópico - DC/CC

O desenvolvimento de software em sistemas embarcados aviônicos é regido por normas rigorosas, entre as quais a DO-178 se destaca como uma das mais importantes. Esta norma fornece diretrizes para garantir a segurança e a confiabilidade do software em sistemas críticos utilizados na aviação. A DO-178 estabelece orientações para as etapas de desenvolvimento do software, desde o planejamento do processo de desenvolvimento até a verificação e validação do software, assegurando que todas as etapas sejam cumpridas de acordo com os padrões exigidos pela indústria aeronáutica [Rapita Systems s.d.].

As decisões das etapas iniciais no desenvolvimento de software impactam em todas as etapas seguintes, como por exemplo, na arquitetura do software são definidos os componentes, ou seja, as partes do software que representam uma funcionalidade do sistema. Esses componentes são fundamentais para a eficiência da análise de cobertura de acoplamento de dados e controle (Data Coupling - DC e Control Coupling - CC) durante a fase de verificação [Rapita Systems s.d.].

O DC/CC ocorre entre componentes de software que estão separados dentro da arquitetura, o que torna essencial a consideração antecipada dessas interações para assegurar que as interfaces e dependências entre os componentes sejam corretamente definidas e testadas. Conceitualmente, Acoplamento de Dados (DC) refere-se à dependência de um componente de software em dados que não estão sob seu controle exclusivo. Já o Acoplamento de Controle (CC) está relacionado ao grau em que um componente influencia a execução de outro. Esses conceitos são fundamentais para a segurança e a funcionalidade de sistemas embarcados, uma vez que falhas na gestão de acoplamento podem levar a comportamentos indesejados ou até mesmo a falhas catastróficas no sistema [Rierson 2012].

O DC/CC é considerado um critério de cobertura estrutural dentro do processo de verificação de software conforme a DO-178C. A cobertura estrutural utiliza testes baseados em requisitos. Essa cobertura é essencial para garantir que as partes críticas do código foram testadas, identificando funções corretas, incorretas ou ausentes. No contexto de DC/CC, a cobertura estrutural demonstra que as interações intencionais entre os componentes foram verificadas, bem como a ausência de interações não intencionais [FEDERAL AVIATION ADMINISTRATION, 2007].

A verificação de DC/CC pode ser desenvolvida em três etapas [FEDERAL AVIATION ADMINISTRATION, 2007]: 
- Identificação das Dependências entre Componentes: Nesta fase, as dependências de sequenciamento, temporização, controle e dados entre os componentes são identificadas. Dependência de sequenciamento refere-se a ordem de execução dos componentes. Dependência de tempo refere-se ao tempo de execução de cada componente individualmente e do tempo de execução da sequência de múltiplos componentes.
- Identificação dos Métodos de Verificação: Após a identificação das dependências, são determinados os métodos de verificação mais adequados, como revisões, análises, testes e rastreabilidade.
- Justificativa para Ausência de Verificação: Caso não haja métodos de verificação disponíveis para alguma dependência, é necessário fornecer uma justificativa documentada para a ausência de verificação, garantindo que todos os aspectos críticos foram considerados.

No contexto deste Trabalho de Conclusão de Curso (TCC), o objetivo é desenvolver uma Ferramenta capaz de executar um conjunto de casos de testes e determinar a cobertura DC/CC de um código. Dentro do escopo do método de verificação, que inclui a realização de testes, o uso de ferramentas automatizadas é essencial para assegurar a eficiência e a precisão na análise de cobertura de acoplamento. Tais ferramentas devem ser capazes de fornecer resultados detalhados sobre a cobertura de acoplamento de dados e controle. De acordo com a tabela apresentada por Leanna Rierson, um dos itens que pode ser verificado inclui o teste para verificar se as entradas das funções são exercidas com valores distintos e se tais valores afetam as saídas. Sendo este o principal critério a ser considerado no TCC.

Referências:

RIERSON, Leanna. Developing Safety-Critical Software: a practical guide for aviation software and do-178c compliance. Nova York: Crc Press, 2012.

FEDERAL AVIATION ADMINISTRATION. Object-Oriented Technology Verification Phase 2 Handbook— Data Coupling and Control Coupling. Washington: S.e., 2007.

RAPITA SYSTEMS. Handbook Efficient verification through the DO-178C life cycle. S.L: S.e., .
