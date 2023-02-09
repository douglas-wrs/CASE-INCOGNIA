# README


### Environment

* Ubuntu 22.04.1 LTS
* conda 22.11.1
* Python 3.8.0

Execute the following commands to download the dataset and install the required packages

```
export INCOGNIA_CASE_PASSWORD=given_password
source ~/.bashrc
bash download.sh
conda create --name incognia python=3.8
conda activate incognia
pip install --pre -U pycaret
pip install -r requirements.txt
```

The command below will start the app
```
streamlit run app.py
```
