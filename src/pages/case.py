import streamlit as st
import pandas as pd

def show():
    st.write('# Incognia | Case Research')

    st.write('### Introdução sobre a Incognia')

    st.markdown("""
    A Incognia é uma solução de biometria comportamental por geolocalização que ajuda aplicativos mobile, especialmente dos setores financeiro e varejo, a aumentar a conversão de transações, reduzir fricção e reduzir fraudes.
    
    A solução consiste em um SDK embarcado no aplicativo do cliente, que uma vez disponibilizado na loja, App Store ou Google Play, começa a capturar dados de localização do usuário ao longo do seu dia. A captura desses dados permite a criação de um padrão único de comportamento para cada usuário, e não depende em nada de nenhum dado de identificação civil como nome, CPF, email ou telefone. Atualmente o SDK da Incognia está embarcado em mais de 100 milhões de dispositivos no Brasil, o que forma um grande efeito de rede. Esse perfil comportamental é usado para autenticar eventos no aplicativo em diversos momentos da jornada do usuário, como no onboarding/abertura de conta, login/acesso, e, por fim, na transação.    
    """)

    st.write('### O case')

    st.markdown("""
    Abaixo seguem os links para duas tabelas, com dados de eventos de logins e transações de bases de duas bases distintas de usuários (ou seja, as bases não estão relacionadas entre si).
    
    Para a avaliação você pode escolher uma das bases e criar uma metodologia para encontrar casos de fraude (roubos de contas [*ato] ou chargebacks).
    
    Sinta-se livre para usar qualquer ferramenta ou métricas de sucesso. Nos envie uma documentação técnica dos resultados com explicações das suas decisões na construção de regras, modelos e das métricas de sucesso.

    O que vamos observar na avaliação:
    
    * Metodologia;
    * Qualidade dos resultados;
    * Qualidade da documentação;
    * Viabilidade de colocar solução desenvolvida em produção.
    
    *ato = account takeover

    Links para download das bases:

    https://drive.google.com/file/d/1WE1lWdCd9goa7cRnOgeQq_2qHEdjxrSQ/view?usp=sharing
    
    A senha de abertura do Zip será compartilhada assim que você responder o email em que o case foi enviado solicitando ela.
    
    Você terá 7 dias após o envio da senha para preparar os resultados e nos enviar o relatório, então marcaremos uma nova conversa para conversarmos sobre os resultados.
    """)

