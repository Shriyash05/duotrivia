SUBSCRIPTION="Azure for Students"
RESOURCEGROUP="appsvc_linux_centralus"
LOCATION="centralus"
PLANNAME="appsvc_linux_centralus"
PLANSKU="F1"
SITENAME="duotrivia"
RUNTIME="PYTHON|3.12"

# gunicorn --bind=0.0.0.0 --timeout 600 main:myapp
python main.py