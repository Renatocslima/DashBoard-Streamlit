import streamlit as st

def main():
    st.title("Página de Input no Streamlit")

    # Input de texto
    nome = st.text_input("Digite seu nome")

    # Input numérico
    idade = st.number_input("Digite sua idade", min_value=0, max_value=100, step=1)

    # Caixa de seleção
    genero = st.selectbox("Selecione seu gênero", ["Masculino", "Feminino", "Outro"])

    # Slider para selecionar um valor numérico
    salario = st.slider("Selecione seu salário", min_value=0, max_value=100000, step=1000)

    # Botão para submissão
    if st.button("Submeter"):
        st.write(f"Nome: {nome}")
        st.write(f"Idade: {idade}")
        st.write(f"Gênero: {genero}")
        st.write(f"Salário: R${salario:.2f}")

if __name__ == "__main__":
    main()


