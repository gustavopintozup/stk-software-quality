# Stack Software Quality

This stack is an unblrella for plugins that inspect the software quality of Java programs.

Currently, we have two plugins imported in this stack:

- **CDD plugin**: A static analysis plugin that computes CDD metrics.
- **Sorald plugin**: A automatic repair plugin that fixes SonarQube violations. 

### Sorald plugin


Esse plugin utiliza a bibilioteca [sorald](https://github.com/SpoonLabs/sorald) para realização de reparos automáticos em programas Java que violem um conjunto de regras do SonarQube.

### Utilização

Para utilizar esse plugin, você precisa primeiro ter o o stk da StackSpot funcionando no seu computador. Para instalar a StackSpot, clique [aqui](https://stackspot.com/).

Em seguida, você precisa importar essa stack deste repositório na sua instalação do stk:

```
stk import stack git@github.com:gustavopintozup/stk-software-quality.git
```

Para garantir que tanto a stack, quanto o plugin, foram importados corretamente, você pode executar os seguintes comandos:

```
stk list stack

stk list plugin
```

Após instalação da stack, basta rodar o plugin dentro do diretório do projeto que você deseja realizar as reparações.

```bash
cd <diretorio-do-projeto-para-reparar>
stk apply plugin -p <diretorio-da-minha-stack>/stk-software-quality/stk-sonarqube-repair-plugin
```

Ao executar o comando, o plugin irá 1) fazer análise estática da base de código do diretório corrente em busca de trechos de código que violassem regras do SonarQube, para depois 2) pergunta ao usuário quais dessas regras devem ser reparadas.

## License
This repository is licensed under MIT.