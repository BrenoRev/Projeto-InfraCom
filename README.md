### Sobre

[Descrição do projeto](https://docs.google.com/document/d/1iQzg-XgjGhXc0kS5K55MEYTc49dtKAfd2NUvQ6UgyBE/edit?usp=sharing)

[Relatório](https://docs.google.com/document/d/1GLGYV3qvB-EYZXF9Jmfv50l0UKK6qs_F7HAPR_Tu1KY/edit?usp=sharing)

<hr>

Para rodar o projeto com sucesso, é necessário executar uma série de comandos essenciais. Inicialmente, é fundamental instalar as dependências do projeto utilizando o comando "pip install -r requirements.txt", garantindo que todas as bibliotecas necessárias estejam disponíveis. Em seguida, para iniciar a execução do sistema, os arquivos "broadcaster.py", "main.py" e "certificate_authority.py" devem ser executados utilizando o interpretador Python, respectivamente. O arquivo "broadcaster.py" é responsável por gerenciar o servidor de broadcast, enquanto "main.py" é o ponto de entrada principal da aplicação, e "certificate_authority.py" implementa a funcionalidade da Autoridade Certificadora para garantir a segurança da comunicação entre os servidores. Esses comandos são cruciais para o funcionamento adequado do projeto, garantindo uma implementação bem-sucedida das etapas de topologia, comunicação, segurança e roteamento dentro da rede de servidores.

Este projeto foi desenvolvido em diversas etapas, começando pela configuração da topologia e comunicação entre os elementos, seguida pela implementação da Autoridade Certificadora para garantir a segurança da comunicação, e finalizando com o estabelecimento de um sistema de roteamento eficiente e um servidor de broadcast para disseminação de mensagens entre os servidores. Cada etapa foi cuidadosamente planejada e implementada, enfrentando desafios específicos que foram superados através de testes e ajustes meticulosos. O resultado é um sistema robusto e funcional, capaz de garantir uma comunicação eficaz e segura dentro da rede de servidores.

Segue um roteiro resumido da ordem para executar o projeto:

```python
pip install -r requirements.txt
python broadcaster.py
python main.py
python certificate_authority.py
```

![image](https://github.com/BrenoRev/Sockets/assets/84048306/0d58cbd9-703e-4c6b-a583-cd160c0676c7)

#### Primeira etapa: Topologia e Comunicação entre elementos:

Na primeira etapa do projeto, focamos na topologia e comunicação entre elementos. Para isso, utilizamos a imagem da Figura 1 do relatório como referência para criar os computadores (PCs) e estabelecer os relacionamentos entre eles. No começo tivemos dificuldade de entender como poderíamos fazer os PCs se comunicarem entre si na implementação até que  nossa abordagem envolveu a criação de uma estrutura de dados que representasse um array com os vínculos de cada PC na rede.

Além disso, atribuímos endereços IP a cada PC, garantindo que houvesse uma identificação única para cada dispositivo na rede. Isso foi fundamental para possibilitar a comunicação eficiente entre os diferentes elementos.

Uma vez que a infraestrutura básica estava estabelecida, implementamos o algoritmo de Dijkstra para determinar o melhor caminho entre os PCs. Esse algoritmo foi escolhido por sua eficiência em encontrar o menor caminho em um grafo, o que é essencial para garantir uma comunicação eficaz na rede.

#### Segunda etapa do projeto

Tínhamos como objetivo implementar uma Autoridade Certificadora (CA) para garantir a segurança da comunicação entre os servidores. Para isso, planejamos que a CA fosse responsável por gerar e distribuir chaves privadas para os servidores, além de verificar a autenticidade das mensagens assinadas pelos mesmos.

Na prática, implementamos essa funcionalidade da CA de forma eficaz. Utilizamos a biblioteca cryptography para gerar chaves privadas e verificar assinaturas digitais, garantindo um alto nível de segurança na comunicação entre os servidores. Além disso, estabelecemos a comunicação entre a CA e os servidores utilizando sockets UDP, o que proporcionou uma comunicação eficiente e assíncrona.

Durante a implementação, não encontramos dificuldades significativas. Todas as funcionalidades da Autoridade Certificadora foram implementadas conforme planejado, garantindo a integridade e a segurança da comunicação entre os servidores.

#### Terceira etapa

Desenvolvemos uma aplicação de chat seguro utilizando o Protocolo UDP, permitindo que os servidores de uma rede se comuniquem entre si de forma assíncrona, tratando e encaminhando mensagens conforme necessário. Detalhando como isso ocorre, temos os métodos utilizados: 

Validação da Mensagem de Broadcast que verifica se a mensagem recebida é uma mensagem de broadcast, se for utilizar a função treat_message_from_broadcaster(decoded_message) é chamada para tratar a mensagem.

Validação de Mensagem Normal verifica se não for uma mensagem pro Broadcast ela é considerada uma menssagem normal,usando a função validate_normal_message(decoded_message) verifica se a mensagem está no formato esperado(composto pelo id do sender seguido do “-” e a mensagem propriamente dita). se o formato for correto o código prossegue para processá-la. 

Validação do Caminho da Mensagem se o remetente da mensagem estiver especificado com um caminho, o código verifica se o caminho está no formato esperado, Se o caminho não estiver no formato correto, a mensagem é descartada.

Verificação da permissão do remetente O código verifica se o remetente da mensagem é um remetente permitido Se o remetente for permitido (ou seja, estiver na lista de relacionamentos do nó atual), a mensagem é considerada válida e processada, caso contrário, é registrada uma mensagem de erro indicando que a mensagem foi recebida de um remetente não permitido.

Usamos também um Tratamento de Exceções foi usado um bloco try-except para capturar e lidar com exceções que possam ocorrer durante o processamento da mensagem Se ocorrer uma exceção, o código registra uma mensagem de erro indicando o tipo de exceção que ocorreu. 

O remetente (Sender) certo é identificado pela validação do ID do remetente em relação aos relacionamentos definidos para cada nó na rede isso é feito pela função  validate_message_is_allowed(sender_id) que verifica se o ID do remetente está presente na lista de relacionamentos do nó atual.

#### Quarta etapa do projeto

Nossa meta era estabelecer um sistema de roteamento eficiente para garantir que as mensagens fossem entregues ao destino correto na rede, levando em conta a topologia da rede e os caminhos disponíveis entre os servidores. Além disso, planejamos implementar um sistema de broadcast de mensagens para permitir que um servidor enviasse uma mensagem para todos os outros servidores na rede.

Para alcançar esses objetivos, optamos por implementar um algoritmo de roteamento baseado no algoritmo de Dijkstra, que calcula o caminho mais curto entre os servidores na rede. Utilizamos sockets UDP para facilitar a comunicação entre os servidores, permitindo uma troca rápida e assíncrona de mensagens. Além disso, desenvolvemos um servidor de broadcast dedicado, responsável por receber mensagens de outros servidores, transformá-las em mensagens de broadcast e enviá-las para todos os outros servidores na lista de endereços de destino.

Durante a implementação, enfrentamos desafios na garantia de que as mensagens de broadcast fossem entregues a todos os servidores na rede de forma eficiente e sem perda de dados. Esse aspecto se mostrou particularmente desafiador em uma rede com múltiplos servidores e possíveis problemas de latência ou perda de pacotes. No entanto, por meio de testes e ajustes cuidadosos, conseguimos superar esses desafios e alcançar um sistema de roteamento e broadcast funcional e robusto.




