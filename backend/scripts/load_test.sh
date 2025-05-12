#!/bin/bash

run_test() {
    local name=$1
    local total=$2
    local concurrent=$3
    local duration=$4

    echo "=== Executando teste: $name ==="
    echo "Total de requisições: $total"
    echo "Requisições concorrentes: $concurrent"
    echo "Duração: $duration segundos"
    echo ""

    hey -n $total \
        -c $concurrent \
        -t $duration \
        -m POST \
        -H "Content-Type: application/json" \
        -d '{"participante_id": "38333828-65c8-447b-91d5-d8b5365c7b1e"}' \
        http://localhost:8000/api/teste/votacao

    echo ""
    echo "=== Fim do teste: $name ==="
    echo ""
    echo "Aguardando 5 segundos antes do próximo teste..."
    sleep 5
}

# Teste 1: Carga baixa
run_test "Carga Baixa" 100 10 30

# Teste 2: Carga média
run_test "Carga Média" 500 50 30

# Teste 3: Carga alta
run_test "Carga Alta" 1000 100 30

# Teste 4: Pico de carga
run_test "Pico de Carga" 2000 200 30

# Teste 5: Carga sustentada
run_test "Carga Sustentada" 5000 100 120 