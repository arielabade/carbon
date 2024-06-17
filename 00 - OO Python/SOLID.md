# Metodologia SOLID em Programação

A metodologia SOLID é um conjunto de princípios de design de software orientado a objetos que visa tornar os sistemas mais compreensíveis, flexíveis e manteníveis. Cada letra de SOLID representa um princípio específico:

## 1. Single Responsibility Principle (SRP) - Princípio da Responsabilidade Única
Uma classe deve ter apenas uma razão para mudar, ou seja, deve ter uma única responsabilidade ou propósito.

## 2. Open/Closed Principle (OCP) - Princípio Aberto/Fechado
As entidades de software (classes, módulos, funções, etc.) devem ser abertas para extensão, mas fechadas para modificação. Isso significa que o comportamento de uma entidade pode ser estendido sem alterar seu código-fonte.

## 3. Liskov Substitution Principle (LSP) - Princípio da Substituição de Liskov
Subtipos devem ser substituíveis por seus tipos base sem alterar a correção do programa. Isso implica que uma classe derivada deve ser capaz de substituir sua classe base sem que o usuário da classe perceba.

## 4. Interface Segregation Principle (ISP) - Princípio da Segregação de Interface
Os clientes não devem ser forçados a depender de interfaces que não utilizam. Em vez disso, muitas interfaces específicas devem ser criadas ao invés de uma única interface genérica.

## 5. Dependency Inversion Principle (DIP) - Princípio da Inversão de Dependência
Módulos de alto nível não devem depender de módulos de baixo nível. Ambos devem depender de abstrações. Além disso, abstrações não devem depender de detalhes; os detalhes devem depender das abstrações.

## Exemplos de Aplicação de Cada Princípio

### 1. SRP
Em uma aplicação de gestão de pedidos, separar a lógica de cálculo de impostos da lógica de envio de pedidos em classes diferentes.

### 2. OCP
Projetar uma classe de cálculo de descontos que permite adicionar novos tipos de desconto sem modificar o código existente da classe.

### 3. LSP
Se temos uma classe `Ave` e uma subclasse `Pinguim`, o `Pinguim` deve ser substituível pela `Ave` sem que os métodos que usam `Ave` quebrem.

### 4. ISP
Em vez de ter uma única interface `Funcionario` com métodos `trabalhar()`, `receberSalario()`, e `obterBeneficios()`, dividir em interfaces menores, como `Trabalhador` e `Beneficiado`.

### 5. DIP
Em vez de uma classe de serviço de e-mail depender diretamente de uma classe concreta de envio de e-mails, ela deve depender de uma interface `EmailService`, permitindo que diferentes implementações de `EmailService` sejam injetadas.

A adoção dos princípios SOLID resulta em um código mais modular, testável e resiliente a mudanças, facilitando a evolução e manutenção do software ao longo do tempo.
