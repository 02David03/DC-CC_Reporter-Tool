1. Análise DC/CC 
  1.1 Introdução
  Acoplamento de dados (Data Coupling - DC) é a dependência de um componente de software em dados que estão além do seu controle exclusivo. Se os dados não forem manipulados corretamente, isso pode resultar na falha da troca dos dados entre módulos ou funções.
  Por outro lado, o Acoplamento de controle (Control Coupling - CC) refere-se à maneira pela qual um componente de software pode impactar a execução de outros. Isso acontece com frequência quando uma função controla a lógica da execução de outra, podendo trazer riscos caso esse controle não seja gerenciado corretamente. 
  A avaliação do Acoplamento de dados (Data Coupling - DC) e  do Acoplamento de controle (Control Coupling - CC) é crucial para o desenvolvimento de software em sistemas críticos de segurança. O uso adequado dessas análises pode prevenir graves falhas em sistemas onde segurança e confiabilidade são prioritárias [1].
  
  1.2 Relevância no Desenvolvimento de Software Crítico
  Em projetos de desenvolvimento de software crítico, especialmente naquelas que são implementados seguindo a norma DO-178B/C, é fundamental realizar a análise do Acoplamento de Dados e Controle (DC/CC) para assegurar que o sistema seja seguro e confiável. O cumprimento da exigência estrutural pela DO-178B/C requer a cobertura completa das análises dos acoplamentos entre os dados e controle no código-fonte, garantindo assim o teste abrangente das rotas relevantes e interações seguras entre componentes [1].
  
  1.3  Técnicas de Detecção de Falhas
  Um problema de Acoplamento de controle (Control Coupling - CC) pode surgir quando uma função é chamada através de um ponteiro, mas nem todas as funções possíveis que o mesmo poderá referenciar são verificadas. Já para o Acoplamento de dados (Data Coupling - DC), em caso de falha, ocorre a utilização de uma variável global antes da inicialização adequada por outro componente.
  A identificação dessas falhas pode ser feita combinando análise estática e dinâmica. A análise estática examina o código em busca de padrões suspeitos, enquanto a análise dinâmica verifica se esses padrões são válidos durante a execução do software para garantir que os testes cubram todos os possíveis cenários [1].
  
  1.4 Ferramentas de Análise e Certificação
  Existem ferramentas que auxiliam na análise DC/CC de um software. Um exemplo é a LDRA, que é uma ferramenta responsável por automatizar a maior parte da análise do acoplamento. A aplicação permite uma minuciosa análise estática para detectar ambiguidades e erros no fluxo dos dados e controle. Adicionalmente, fornece também uma avaliação dinâmica que verifica o adequado alcance de cobertura do código durante os testes realizados, garantindo assim a exploração abrangente de todos possíveis caminhos na execução e utilização dos dados Este conjunto de análises auxilia na validação e na conformação dos requisitos estabelecidos pela norma DO-178B/C para certificação, comprovando que o software atende às necessidades essenciais da segurança e confiabilidade [1].


2. Instrumentação
  2.1 Introdução
  Instrumentação, no contexto do desenvolvimento de software, refere-se à inserção de pontos de verificação em um programa para monitorar sua execução sem comprometer a funcionalidade original. Essa técnica é valiosa na avaliação da cobertura do código durante os testes e garante que todas as funções do sistema sejam executadas pelo menos uma vez, reduzindo assim o risco de falhas inesperadas em etapas posteriores [2]. 
  
  2.2 Tipos e Características da Instrumentação
  Existem dois tipos principais de ferramentas de instrumentação:
  Interativas: demandam que o usuário participe ativamente durante a execução, habilitando inserção de pontos de parada e monitoramento do andamento da programação em tempo real. Um exemplo é o depurador simbólico “gdb” [2].
  Não-interativas: Executam automaticamente e fornecem relatórios detalhados sobre eventos monitorados após a conclusão da análise. Esse processo é denominado de análise “post mortem” [2].
  Os fatores principais da instrumentação são: a ausência de perturbação no serviço original do programa, juntamente com um monitoramento constante durante a execução e o consumo extra de recursos. Isso resulta em um custo tanto para o desenvolvimento como para a execução [2].
  
  2.3 Vantagens e Problemas da Instrumentação
  A utilizaççao de instrumentação proporciona diversos benefícios, incluindo a gestão eficaz de riscos através da entrega precisa de dados e abrangente cobertura sobre o código, identificação dos casos redundantes ou faltantes em testes e ainda melhora no processo de desenvolvimento ao não permitir falhas passarem despercebidas para as etapas posteriores. No entanto, inserção de código tem como consequência um aumento no tamanho do código (overhead de código) e no tempo de execução (overhead de execução). Sendo assim, a instrumentação de programas traz consigo um grande custo associado.
  
  
  
Referências
    [1] HENNELL, M. A. Data Coupling and Control Coupling. v. 1.0. Reino Unido: LDRA, 2014.
    [2] COSTA, Harry Trinta P. Técnicas de instrumentação e coleta de rastros de execução. São Carlos: Instituto de Ciências Matemáticas e de Computação – Universidade de São Paulo, 2007.
    
