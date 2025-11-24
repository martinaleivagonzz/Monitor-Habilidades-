Activar entorno virtual:
# Verifica qué entorno virtual tienes
ls -la | grep venv

# Si tienes venv/
source venv/bin/activate

# O si tienes monitor_env/
source monitor_env/bin/activate

# Luego instala streamlit
pip install streamlit

# Y ejecuta
streamlit run dashboard.py


