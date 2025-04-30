
import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(page_title="Radar de FIIs", layout="wide")

st.title("Radar Automático de Fundos Imobiliários (FIIs)")
st.markdown("""
Este sistema analisa automaticamente uma lista de FIIs e identifica os que têm maior potencial de **compra** com base em análise técnica (médias móveis e RSI).
""")

fii_lista = ["BTLG11.SA", "KNCR11.SA", "XPML11.SA", "RBRR11.SA", "MCCI11.SA"]
period = st.selectbox("Escolha o período de análise", ["3mo", "6mo", "1y"])

resultados = []

for ticker in fii_lista:
    try:
        data = yf.download(ticker, period=period)
        if data.empty:
            continue

        data["SMA20"] = data["Close"].rolling(20).mean()
        data["SMA50"] = data["Close"].rolling(50).mean()
        rsi = ta.momentum.RSIIndicator(data["Close"]).rsi()

        sma20 = data["SMA20"].iloc[-1]
        sma50 = data["SMA50"].iloc[-1]
        rsi_val = rsi.iloc[-1]

        if sma20 > sma50 and 40 < rsi_val < 70:
            recomendacao = "Comprar"
        elif rsi_val >= 70:
            recomendacao = "Esperar (Sobrecomprado)"
        else:
            recomendacao = "Manter ou Aguardar"

        resultados.append({
            "FII": ticker.replace(".SA", ""),
            "SMA20 > SMA50": "Sim" if sma20 > sma50 else "Não",
            "RSI": round(rsi_val, 2),
            "Recomendação": recomendacao
        })

    except Exception as e:
        st.error(f"Erro ao processar {ticker}: {e}")

if resultados:
    df_resultado = pd.DataFrame(resultados)
    st.subheader("Resultados da Análise")
    st.dataframe(df_resultado)
else:
    st.warning("Nenhum resultado encontrado. Verifique os dados ou o período selecionado.")
