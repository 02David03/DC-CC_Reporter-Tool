Modularizar a arquitetura de um *software* traz vantagens para a administração do trabalho, alocar pessoas em paralelo para que o projeto possa progredir rapidamente ou usar módulos pré-prontos ou vindos externamente para conseguir dedicação maior às características de uma nova situação. Entretanto é-se criada uma necessidade, os módulos precisam se comunicar para atingir a finalidade do sistema, e toda vez que dados são passados de um lugar para outro eles podem se corromper ou acabarem sendo usados da maneira errada (FISHER, 2007, p. 106).

Para um time de V&V (Verificação e Validação), o cuidado com as interfaces acaba sendo constante em todas as fases (requisitos, arquitetura, implementação e testes). Enquanto a divisão em módulos não faz sentido somente para o gerenciamento do projeto, pois o problema abordado também é reduzido em partes para os engenheiros abordarem, o que acontece é ser necessário que haja os responsáveis por garantir que a junção dos módulos corresponda ao sistema final. Essa incumbência geralmente é do time de sistemas e de V&V.

Em se tratando de sistemas complexos, a análise de interfaces não pode ser subestimada e Fisher (2007, p. 121) traz 5 pontos: garantir que os desenvolvedores possuam as interfaces certas definidas, é importante que o pessoal de V&V faça sua avaliação independente de que dados trafegarão entre os componentes do sistema e por quais interfaces, deste modo eles podem comparar com o que os desenvolvedores definem; as interfaces devem estar totalmente descritas; as interfaces devem ser usadas consistentemente através do sistema; manter as necessidades de performance mesmo com o uso dessas interfaces; as interfaces devem ser testáveis.

Destaca-se a natureza integradora dessas atividades: a qualidade das interfaces não serão avaliadas nos artefatos em si, o time de V&V, por meio de seu planejamento, quer saber o atendimento a um determinado objetivo. Fisher (2007) traz como exemplo o objetivo de garantir que as interfaces de *software* identificam e lidam com defeitos.

Para testar e avaliar as interfaces em primeiro momento, pode-se usar modelos. Isto implica em custos adicionais para o time de V&V do que simplesmente rodar código pronto para verificação. Contudo, como Laski e Stanley (2009, p. 32 e 33) caracterizam o refinamento Top-Down, o código executável pode ser a última das iterações que produzem aprimoramentos graduais no modelo de maneira que entre duas etapas consecutivas seja relativamente fácil de verificar que o novo modelo cumpre com os objetivos do anterior só que com mais detalhes. O que seria visto como o primeiro modelo, o mais geral e abstrato, é a especificação do problema dada pelo planejamento; o último é a implementação numa linguagem de programação.

Isto vem com a ideia de construir um *software* com qualidade por design ao invés de medi-la depois (LASKI; STANLEY, 2009, p. 25). Idealmente, como corretude é a característica indispensável da qualidade, ela seria provada passo a passo pelas iterações de modelo supramencionadas.

FISHER, Marcus S. *Software Verification and Validation*: An Engineering and Scientific Approach. Nova York: Springer, 2007.

LASKI, Janusz; STANLEY, William. *Software Verification and Analysis*: An Integrated, Hands-On Approach. Londres: Springer, 2009.



