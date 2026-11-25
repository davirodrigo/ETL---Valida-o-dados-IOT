import math
import pandas as pd

#START BLOCK 1

def processar_lote(eventos: list[dict]) -> tuple[pd.DataFrame, pd.DataFrame]:

    if not eventos:
        return pd.DataFrame(), pd.DataFrame()

    #consideramos cargas que não retornam dados para poupar processamento

#END BLOCK 1



#START BLOCK 2

    df = pd.DataFrame(eventos).copy()

    df["timestamp_leitura"] = pd.to_datetime(
        df["timestamp_leitura"], errors="coerce", utc=True
    )
    df["timestamp_envio"] = pd.to_datetime(
        df["timestamp_envio"], errors="coerce", utc=True
    )
    df["rotacoes"] = pd.to_numeric(df["rotacoes"], errors="coerce")
    df["raio_roda_m"] = pd.to_numeric(df["raio_roda_m"], errors="coerce")
    df["tensao_v"] = pd.to_numeric(df["tensao_v"], errors="coerce")

#END BLOCK 2




#START BLOCK 3

    # Identifica motivos de erro
    motivos = []
    for idx, row in df.iterrows():
        erros_linha = []
        if pd.isna(row["timestamp_leitura"]) or pd.isna(row["timestamp_envio"]):
            erros_linha.append("timestamp_invalido")
        if pd.isna(row["rotacoes"]) or row["rotacoes"] < 0:
            erros_linha.append("rotacoes_invalidas")
        if pd.isna(row["raio_roda_m"]) or row["raio_roda_m"] <= 0:
            erros_linha.append("raio_invalido")
        if not pd.isna(row["tensao_v"]) and row["tensao_v"] < 11.0:
            erros_linha.append("tensao_baixa_sim800l")
        motivos.append(",".join(erros_linha) if erros_linha else None)

    df["motivo_erro"] = motivos


#END BLOCK 3


#START BLOCK 4

    df_erros = df[df["motivo_erro"].notna()].copy()
    df_validos = df[df["motivo_erro"].isna()].copy()


#END BLOCK 4




#START BLOCK 5

    if not df_validos.empty:
        df_validos = df_validos.drop_duplicates(subset=["evento_id"])
        df_validos["distancia_m"] = (
            df_validos["rotacoes"] * (2 * math.pi * df_validos["raio_roda_m"])
        )
        df_validos["distancia_km"] = df_validos["distancia_m"] / 1000.0
        df_validos["latencia_envio_s"] = (
            df_validos["timestamp_envio"] - df_validos["timestamp_leitura"]
        ).dt.total_seconds().round(2)

    return df_validos, df_erros

#END BLOCK 5