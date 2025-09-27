
import pathlib
import requests
import sqlalchemy as sa
import pandas as pd
from time import time
import argparse
import pyarrow.parquet as pq

def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    output_path = pathlib.Path("yellow_tripdata.parquet")          # or "output.csv.gz"

    response = requests.get(url, stream=True, verify=False)
    
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)

    # Baixa csv
    #os.system(f'wget {url} -O {output_path}') # Baixa na url e salva como output_path


    # Conecta SQl
    engine = sa.create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    batch_size = 100000
    pq_file = pq.ParquetFile(output_path)

    # Lê csv (iterativo)
    batch_iter = iter(pq_file.iter_batches(batch_size=batch_size)) # Lê 100k por vez, base com 1.6M

    df_first_100k = next(batch_iter)
    df_first_100k = df_first_100k.to_pandas()

    # Transforma datetime
    df_first_100k['tpep_pickup_datetime'] = pd.to_datetime(df_first_100k['tpep_pickup_datetime'])
    df_first_100k['tpep_dropoff_datetime'] = pd.to_datetime(df_first_100k['tpep_dropoff_datetime'])

    df_cabecalho = df_first_100k.head(0)

    #print(pd.io.sql.get_schema(df_cabecalho, name='tb_yellow_tripdata', con=engine))

    # Cria tabela sobe primeiros 100k
    df_cabecalho.to_sql(name=table_name, con=engine, if_exists='replace')
    df_first_100k.to_sql(name=table_name, con=engine, if_exists='append')

    while True: #(Vai dar erro quando não houver mais dados)

        try:

            t_start = time()

            df_temp = next(batch_iter)
            df_temp = df_temp.to_pandas()

            df_temp['tpep_pickup_datetime'] = pd.to_datetime(df_temp['tpep_pickup_datetime'])
            df_temp['tpep_dropoff_datetime'] = pd.to_datetime(df_temp['tpep_dropoff_datetime'])

            df_temp.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk..., took %.3f seconds' % (t_end - t_start))
            
        except:
            print('Finalizado!!')
            break



if __name__ == '__main__':
        
    parser = argparse.ArgumentParser(description='Ingestão de dados no Postgres')

    # user, password, host, port, db name, tb name, url do csv
    parser.add_argument('--user', help='username for postgres')           # positional argument
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='Nome da tabela em que os resultados serão escritos')
    parser.add_argument('--url', help='url do arquivo csv')

    args = parser.parse_args()

    main(args)



