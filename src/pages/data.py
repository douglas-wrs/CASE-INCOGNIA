import streamlit as st
import pandas as pd

def show():
    st.write('# Data Dictionary')
    st.write('## Payments')
    st.markdown("""
    | coluna                         | tipo   | descrição                                                                                      |
    |--------------------------------|--------|------------------------------------------------------------------------------------------------|
    | id                             | string | identificador da transação                                                                     |
    | account_id                     | string | identificador da conta                                                                         |
    | device_id                      | string | identificador do dispositivo                                                                   |
    | installation_id                | string | identificador da instalação                                                                    |
    | timestamp                      | long   | timestamp (unixtime - em ms)                                                                   |
    | device_age_ms                  | long   | idade do dispositivo (em ms)                                                                   |
    | n_accounts_by_device_30d       | int    | número de contas acessadas pelo dispositivo nos últimos 30 dias                                |
    | sum_values_by_device_30d       | float  | soma dos valores das transações realizadas pelo dispositivo nos últimos 30 dias                |
    | sum_values_by_device_3d        | float  | soma dos valores das transações realizadas pelo dispositivo nos últimos 3 dias                 |
    | sum_values_by_installation_30d | float  | soma dos valores das transações realizadas pela instalação nos últimos 30 dias                 |
    | sum_values_by_installation_3d  | float  | soma dos valores das transações realizadas pela instalação nos últimos 3 dias                  |
    | low_geo_chargeback_rate_30d    | float  | taxa de chargeback rate da região geográfica associada à transação (precisão geográfica baixa) |
    | medium_geo_chargeback_rate_30d | float  | taxa de chargeback rate da região geográfica associada à transação (precisão geográfica média) |
    | high_geo_chargeback_rate_30d   | float  | taxa de chargeback rate da região geográfica associada à transação (precisão geográfica alta)  |
    | value                          | float  | valor da transação                                                                             |
    | chargedback                    | float  | se a transação ocasionou um chargeback                                                         |
    """)
    st.write('## Logins')
    st.markdown("""
    | coluna                               | tipo   | descrição                                                                                   |
    |--------------------------------------|--------|---------------------------------------------------------------------------------------------|
    | id                                   | string | identificador do login                                                                      |
    | account_id                           | string | identificador da conta                                                                      |
    | device_id                            | string | identificador do dispositivo                                                                |
    | installation_id                      | string | identificador da instalação                                                                 |
    | timestamp                            | long   | timestamp (unixtime - em ms)                                                                |
    | is_from_official_store               | bool   | se o app utilizado foi instalado através de uma loja oficial                                |
    | is_emulator                          | bool   | uso de emulador                                                                             |
    | has_fake_location_app                | bool   | se dispositvo possui applicação de geração de localizações falsas                           |
    | has_fake_location_enabled            | bool   | se dispositivo habilitou  geração de localizações falsas                                    |
    | probable_root                        | bool   | provável root do sistema                                                                    |
    | device_age_ms                        | long   | idade do dispositivo (em ms)                                                                |
    | max_installations_on_related_devices | int    | quantidade máxima de instalações dos dispositivos associados à conta                        |
    | never_permitted_location_on_account  | bool   | se dispositivo nunca habilitou coleta de localizações, quando outros dispositivos o fizeram |
    | boot_count                           | int    | quantidade de reinicializações do dispositivo                                               |
    | wallpaper_count                      | int    | quantidade de wallpapers do dispositivo                                                     |
    | n_accounts                           | int    | número de contas acessadas pelo dispositivo                                                 |
    | ato                                  | bool   | se login está associado a um evento de account takeover                                     |
    
    """)
