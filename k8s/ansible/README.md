Run the ansible playbook to install what is needed for the cluster.

install ansible galaxy deps

ansible-galaxy install -r playbook/requirements.yml


install addons

ansible-playbook playbook/addons.yml 




istio https://istio.io/latest/docs/setup/install/helm/

helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/

helm repo add grafana https://grafana.github.io/helm-charts

