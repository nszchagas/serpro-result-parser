# Serpro Results Parser

## Requirements
- Python
- Docker

## Running 

To run execute in the project's root.

```shell
chmod +x run.sh
./run.sh
```

## Invalid results

Invalid results can happen during parse, they are stored in .sql files with suffix _error. You can manually edit this results, or insert them in the database anyway. They may alter statistics.

## Consulting DB

To make queries in the database you may use the container on interactive mode (`docker exec -u postgres -it postgres psql -d postgres`) or run queries directly from shell (`docker exec -u postgres postgres psql -d postgres -c '<YOU QUERY>'`).

Example: 
```shell 
docker exec -u postgres postgres psql -d postgres -c 'select count(*) from serpro'
```

### Useful tip

To know how many people scored higher (you can include same scores using >=), run the query: 

```sql 
select count(*) from serpro where nfc is not null and nfc > (select nfc from serpro where lower(nome) like lower('Your Name%')); 	
```
