import streamlit as st
import pandas as pd

st.set_page_config(page_title="VAIC vs VAIC ESG", layout="wide")

# =========================
# TÍTULO
# =========================
st.title("VAIC vs VAIC ESG")
st.markdown("Comparação entre o modelo tradicional e o modelo expandido com ESG.")

# =========================
# LAYOUT: INPUTS NA SIDEBAR
# =========================
st.sidebar.header("Inputs")

ebit = st.sidebar.number_input("EBIT", value=500.0)
depreciation = st.sidebar.number_input("Depreciação", value=100.0)
amortization = st.sidebar.number_input("Amortização", value=50.0)
hc = st.sidebar.number_input("Capital Humano (HC)", value=300.0)
ce = st.sidebar.number_input("Capital Empregado (CE)", value=2000.0)
esg_score = st.sidebar.number_input("Escore ESG (0 a 1)", min_value=0.0001, max_value=1.0, value=0.5)

# =========================
# BOTÃO
# =========================
if st.sidebar.button("Calcular"):

    # =========================
    # CÁLCULOS BASE
    # =========================
    va = ebit + depreciation + amortization + hc
    sc = va - hc

    hce = va / hc if hc != 0 else 0
    cee = va / ce if ce != 0 else 0
    sce = sc / va if va != 0 else 0

    # VAIC tradicional
    vaic = hce + cee + sce

    # =========================
    # ESG (TRANSFORMAÇÃO LINEAR)
    # =========================
    ece = esg_score * (sc / va) if va != 0 else 0

    # VAIC ESG
    vaic_esg = vaic + ece

    # =========================
    # RESULTADOS PRINCIPAIS
    # =========================
    st.subheader("🚀 Indicadores principais")

    col1, col2 = st.columns(2)

    col1.metric("VAIC (Tradicional)", f"{vaic:.4f}")
    col2.metric("VAIC ESG", f"{vaic_esg:.4f}", delta=f"{(vaic_esg - vaic):.4f}")

    # =========================
    # COMPONENTES
    # =========================
    st.subheader("📈 Componentes")

    col3, col4, col5, col6 = st.columns(4)

    col3.metric("HCE", f"{hce:.4f}")
    col4.metric("CEE", f"{cee:.4f}")
    col5.metric("SCE", f"{sce:.4f}")
    col6.metric("ECE (ESG)", f"{ece:.4f}")

    # =========================
    # GRÁFICOS LADO A LADO
    # =========================
    st.subheader("📊 Estrutura dos Modelos")

    col_g1, col_g2 = st.columns(2)

    df_vaic = pd.DataFrame({
        "Componentes": ["HCE", "CEE", "SCE"],
        "Valores": [hce, cee, sce]
    }).set_index("Componentes")

    df_vaic_esg = pd.DataFrame({
        "Componentes": ["HCE", "CEE", "SCE", "ECE"],
        "Valores": [hce, cee, sce, ece]
    }).set_index("Componentes")

    with col_g1:
        st.markdown("**VAIC Tradicional**")
        st.bar_chart(df_vaic)

    with col_g2:
        st.markdown("**VAIC ESG**")
        st.bar_chart(df_vaic_esg)

    # =========================
    # INFORMAÇÕES ADICIONAIS
    # =========================
    with st.expander("Detalhes adicionais"):
        st.write(f"VA: {va:.2f}")
        st.write(f"SC: {sc:.2f}")

    # =========================
    # EQUAÇÕES
    # =========================
    st.subheader("📐 Equações dos Modelos")

    st.markdown("**VAIC Tradicional:**")
    st.latex(r"VAIC = HCE + CEE + SCE")

    st.markdown("**Componentes:**")
    st.latex(r"HCE = \frac{VA}{HC}")
    st.latex(r"CEE = \frac{VA}{CE}")
    st.latex(r"SCE = \frac{SC}{VA}")

    st.markdown("**VAIC ESG (Expandido):**")
    st.latex(r"VAIC_{ESG} = HCE + CEE + SCE + ECE")

    st.markdown("**Componente ESG (Transformação Linear):**")
    st.latex(r"ECE = ESG \cdot \frac{SC}{VA}")
