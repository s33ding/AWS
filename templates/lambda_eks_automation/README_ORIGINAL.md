# EKS Scaling Automation

Automação inteligente para escalonamento de nós EKS baseada em horários, otimizando custos sem comprometer performance.

## 📋 Problema

- Não é possível usar Reserved Instances com créditos promocionais
- Necessidade de otimizar custos mantendo performance adequada
- Padrões de uso previsíveis que permitem escalonamento programado

## 🎯 Solução

Sistema automatizado que escala node groups EKS baseado em horários de São Paulo:

### 📅 Cronograma de Escalonamento

```
Horário (São Paulo) | Segunda | Terça | Quarta | Quinta | Sexta | Sábado | Domingo
-------------------|---------|-------|--------|--------|-------|--------|--------
00:00 - 01:00      |   B1    |  B1   |   B1   |   B1   |  B1   |   S1   |   S1
01:00 - 06:30      |   S1    |  S1   |   S1   |   S1   |  S1   |   S1   |   S1
06:30 - 11:30      |   B1    |  B3   |   B1   |   B1   |  B1   |   B1   |   B1
11:30 - 24:00      |   B1    |  B1   |   B1   |   B1   |  B1   |   B1   |   B1
```

**Legenda:**
- **S1**: 1x m5.xlarge (horário de sono)
- **B1**: 1x m5a.4xlarge (operação normal)
- **B3**: 3x m5a.4xlarge (pico de terça-feira)

## 🏗️ Arquitetura

```
EventBridge Rules → Lambda Function → EKS API → DynamoDB Logs
                                   ↓
                              CloudWatch Logs
```

### Componentes:

1. **Lambda Function**: Lógica de escalonamento
2. **DynamoDB**: Logs de atividade
3. **EventBridge**: Agendamento automático
4. **IAM Role**: Permissões necessárias
5. **CloudWatch**: Monitoramento e logs

## 🚀 Deploy

### 1. Preparar ambiente

```bash
cd /home/roberto/Github/aws/templates/lambda_eks_automation
pip install -r requirements.txt
```

### 2. Executar deploy

```bash
python deploy_infrastructure.py
```

O script criará automaticamente:
- ✅ IAM Role com permissões necessárias
- ✅ DynamoDB table para logs
- ✅ Lambda function com o código
- ✅ EventBridge rules para agendamento
- ✅ Permissões entre serviços

### 3. Verificar deploy

```bash
python test_lambda.py
```

## 📊 Monitoramento

### Verificar status atual

```bash
python monitor.py
```

### Logs no CloudWatch

```
/aws/lambda/eks-scaling-automation
```

### Dados no DynamoDB

Tabela: `eks-scaling-logs`
- Timestamp de cada execução
- Tipo de escalonamento aplicado
- Resultados da operação
- Configurações dos node groups

## 💰 Economia Estimada

| Cenário | Custo Diário | Custo Mensal |
|---------|--------------|--------------|
| Sempre 3 nós grandes | $49.54 | $1,486.08 |
| Sempre 1 nó grande | $16.51 | $495.36 |
| **Cronograma atual** | **$14.23** | **$426.72** |

**Economia mensal estimada: $68.64 (13.9%)**

## 🔧 Configuração

### Variáveis de ambiente (Lambda)

```
CLUSTER_NAME=sas-6881323-eks
REGION=sa-east-1
TABLE_NAME=eks-scaling-logs
```

### Node Groups

```python
SMALL_NODEGROUP = 'default-20250319191255393900000026'  # m5.xlarge
BIG_NODEGROUP = 'new-m5a4xlarge-v4'  # m5a.4xlarge
```

## 📈 EventBridge Rules

| Rule | Horário SP | Horário UTC | Descrição |
|------|------------|-------------|-----------|
| sleep-start | 01:00 | 04:00 | Inicia modo sleep |
| morning-start | 06:30 | 09:30 | Inicia operação matinal |
| afternoon-start | 11:30 | 14:30 | Inicia operação vespertina |
| weekend-midnight | 00:00 (Sáb/Dom) | 03:00 | Verificação fim de semana |

## 🧪 Testes

### Testar lógica de escalonamento

```bash
python test_lambda.py
```

### Testar manualmente

```bash
aws lambda invoke \
  --function-name eks-scaling-automation \
  --payload '{"trigger": "manual_test"}' \
  --region sa-east-1 \
  response.json
```

## 🔍 Troubleshooting

### Verificar logs

```bash
aws logs tail /aws/lambda/eks-scaling-automation --follow --region sa-east-1
```

### Verificar node groups

```bash
aws eks describe-nodegroup \
  --cluster-name sas-6881323-eks \
  --nodegroup-name new-m5a4xlarge-v4 \
  --region sa-east-1
```

### Verificar EventBridge rules

```bash
aws events list-rules --name-prefix eks-scaling --region sa-east-1
```

## 🛡️ Segurança

### Permissões IAM mínimas

- `eks:DescribeCluster`
- `eks:DescribeNodegroup`
- `eks:UpdateNodegroupConfig`
- `eks:ListNodegroups`
- `dynamodb:PutItem`
- `logs:CreateLogGroup`
- `logs:CreateLogStream`
- `logs:PutLogEvents`

### Princípio do menor privilégio

O role IAM criado tem apenas as permissões necessárias para:
- Gerenciar node groups do cluster específico
- Escrever logs no DynamoDB
- Criar logs no CloudWatch

## 📞 Suporte

### Logs importantes

1. **CloudWatch Logs**: Execução da Lambda
2. **DynamoDB**: Histórico de escalonamento
3. **EKS Console**: Status dos node groups
4. **EventBridge**: Execução das rules

### Contatos

- **Desenvolvedor**: Roberto
- **Projeto**: EKS Cost Optimization
- **Região**: sa-east-1

## 🔄 Atualizações

### Atualizar código da Lambda

```bash
python deploy_infrastructure.py
```

### Modificar cronograma

Edite as rules no EventBridge ou modifique a função `determine_scaling_action()` no código.

### Adicionar novos node groups

Atualize as constantes `SMALL_NODEGROUP` e `BIG_NODEGROUP` no código.

---

**⚠️ Importante**: O autoscaler do EKS permanece ativo para ajustes dinâmicos conforme a demanda real.
