SUBSCRIPTION="Azure for Students"
RESOURCEGROUP="appsvc_linux_centralus"
LOCATION="centralus"
PLANNAME="appsvc_linux_centralus"
PLANSKU="F1"
SITENAME="duotrivia"
RUNTIME="PYTHON|3.12"

az webapp config set --resource-group $RESOURCEGROUP --name $SITENAME --startup-file "unicorn app.main:app --host 0.0.0.0 --port 8080