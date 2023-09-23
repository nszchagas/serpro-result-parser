#!/bin/bash

# Download file.
if ! [[ -f serpro.pdf ]]; then
    echo "Downloading objective test results..."
    wget -O serpro.pdf https://cdn.cebraspe.org.br/concursos/SERPRO_23/arquivos/ED_3_SERPRO_RES_FIN_OBJ_CONV_PRAT.PDF
fi

# Download prova prática files.
if ! [[ -f serpro_pratica.pdf ]]; then
    echo "Downloading pratical test results..."
    wget -O serpro_pratica.pdf https://cdn.cebraspe.org.br/concursos/SERPRO_23/arquivos/ED_5_SERPRO_RES_PROV_PROVA_PRATICA.PDF
fi

# Run postgres in container
postgres_stats=$(docker container ls | grep "postgres")

if [[ -z $postgres_stats ]]; then
    docker run -e POSTGRES_PASSWORD=postgres --name postgres -d postgres:latest
fi

pipenv install
pipenv shell

# Parse file to serpro.sql
if ! [[ -f serpro.sql ]]; then
    python parse_classificacao.py >serpro.sql 2>serpro_error.sql || {
        echo "Failed to parse classificação."
        rm -f serpro.sql
        exit 1
    }
fi

# Parse file to serpro.sql
if ! [[ -f serpro_pratica.sql ]]; then
    python parse_classificacao_pratica.py >serpro_pratica.sql 2>serpro_pratica_error.sql || {
        echo "Failed to parse classificação prática."
        rm -f serpro_pratica.sql
        exit 1
    }
fi

# Create table for insertions.
docker exec -u postgres postgres psql -d postgres -U postgres -c "create table if not exists serpro (num_inscr varchar(8) primary key, nome varchar(255), crt_pt  int, crt_ing  int, crt_pe  int, crt_rac  int, crt_leg  int, crt_bas  int, crt_esp  int, nt_pt  float, nt_ing  float, nt_pe  float, nt_rac  float, nt_leg  float, nt_bas  float, nt_esp  float, nt_final_obj float)"
docker exec -u postgres postgres psql -d postgres -U postgres -c "alter table serpro add column if not exists nt_final_pratica float"
docker exec -u postgres postgres psql -d postgres -U postgres -c "alter table serpro add column if not exists nfc float generated always as (nt_bas + 2*nt_esp + nt_final_pratica) stored"

docker exec -i -u postgres postgres psql <serpro.sql
docker exec -i -u postgres postgres psql <serpro_pratica.sql

# Create generated column for nota final

# @TODO: remove
# rm serpro.sql serpro_error.sql serpro_pratica.sql serpro_pratica_error.sql -f
