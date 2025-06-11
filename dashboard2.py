import streamlit as st
import pandas as pd
import os

st.set_page_config(layout='wide')

CSV_PATH = 'alugueis.csv'

# Função para carregar o arquivo
def carregar_imoveis():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        if 'desconto_mes' not in df.columns:
            df['desconto_mes'] = 0
        return df
    else:
        # Cria arquivo vazio se não existir
        df = pd.DataFrame(columns=['id','endereco','valor_aluguel','desconto_mes'])
        df.to_csv(CSV_PATH, index=False)
        return df

# Função para salvar as alterações
def salvar_imoveis(df):
    df.to_csv(CSV_PATH, index=False)

# Função de login
def login_form():
    st.markdown("## Login")
    with st.form("login_form", clear_on_submit=True):
        usuario = st.text_input('Usuário')
        senha = st.text_input('Senha', type='password')
        submit = st.form_submit_button('Entrar')
        if submit:
            if usuario == 'biamurad' and senha == 'asilo123':
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error('Credenciais inválidas!')

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([2,2,2])
    with col2:
        login_form()
    st.stop()

# Carregar imóveis do CSV
df = carregar_imoveis()

st.title('Sistema de Gestão de Aluguéis')

# Visão geral
st.markdown("#### Visão Geral")
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Total de Imóveis", len(df))
with m2:
    st.metric("Receita Mensal", f"R$ {df['valor_aluguel'].sum():,.2f}")
with m3:
    st.metric("Previsão Anual", f"R$ {((df['valor_aluguel']-df['desconto_mes']).sum()*12):,.2f}")

# Tabela de imóveis
df['valor_anual'] = (df['valor_aluguel'] - df['desconto_mes']) * 12
st.dataframe(df[['id', 'endereco', 'valor_aluguel', 'desconto_mes', 'valor_anual']], use_container_width=True)

# Adicionar imóvel
st.markdown("---")
st.markdown("#### Adicionar Novo Imóvel")
with st.form("form_add", clear_on_submit=True):
    novo_endereco = st.text_input('Endereço Completo')
    novo_valor = st.number_input('Valor do Aluguel (R$)', min_value=0)
    novo_desconto = st.number_input('Desconto do Mês (R$)', min_value=0)
    submit_add = st.form_submit_button('Salvar Imóvel')
    if submit_add:
        if novo_endereco and novo_valor > 0:
            novo_id = int(df['id'].max()) + 1 if not df.empty else 1
            novo = pd.DataFrame([{
                'id': novo_id,
                'endereco': novo_endereco,
                'valor_aluguel': novo_valor,
                'desconto_mes': novo_desconto
            }])
            df = pd.concat([df, novo], ignore_index=True)
            salvar_imoveis(df)
            st.success("Imóvel adicionado com sucesso!")
            st.rerun()
        else:
            st.error("Preencha o endereço e o valor do aluguel corretamente.")

# Remover imóvel
st.markdown("#### Remover Imóvel")
if not df.empty:
    ids = df['id'].tolist()
    id_remover = st.selectbox('Selecione o ID do Imóvel para Remover', ids)
    if st.button('Remover Imóvel'):
        df = df[df['id'] != id_remover]
        salvar_imoveis(df)
        st.success("Imóvel removido com sucesso!")
        st.rerun()
else:
    st.info("Nenhum imóvel cadastrado para remover.")

# Botão de sair
if st.button('Sair', key='logout', help='Encerrar sessão'):
    st.session_state.logged_in = False
    st.rerun()
