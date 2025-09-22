# Gaming Neo4j Study Project

Este projeto demonstra o uso do Neo4j (banco de dados em grafo) com Python, 
utilizando uma temática de jogos eletrônicos para fins de estudo.

## Estrutura do Projeto

```
gaming_neo4j_study/
├── main.py              # Aplicação principal
├── config/              # Configurações
├── database/            # Conexão com banco
├── models/              # Modelos de dados  
├── repositories/        # Acesso a dados
├── services/           # Lógica de negócio
├── queries/            # Queries Cypher
└── utils/              # Utilitários
```

## Como Executar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Inicie o Neo4j:
```bash
docker-compose up -d
```

3. Execute a aplicação:
```bash
python main.py
```

4. Acesse o Neo4j Browser: http://localhost:7474
   - Usuário: neo4j
   - Senha: password

## Conceitos Demonstrados

- Modelagem de dados em grafo
- Relacionamentos entre entidades
- Queries Cypher
- Padrões de design (Repository, Service)
- Conexão Python + Neo4j