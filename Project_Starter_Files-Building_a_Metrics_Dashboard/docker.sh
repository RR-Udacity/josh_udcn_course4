# build frontend & push to docker hub
cd ~/git/udcn_course4/Project_Starter_Files-Building_a_Metrics_Dashboard/reference-app/frontend
docker build -t jdhaines/ud4-frontend:latest .
docker push jdhaines/ud4-frontend

# build backend & push to docker hub
cd ~/git/udcn_course4/Project_Starter_Files-Building_a_Metrics_Dashboard/reference-app/backend
docker build -t jdhaines/ud4-backend:latest .
docker push jdhaines/ud4-backend

# build trial & push to docker hub
cd ~/git/udcn_course4/Project_Starter_Files-Building_a_Metrics_Dashboard/reference-app/trial
docker build -t jdhaines/ud4-trial:latest .
docker push jdhaines/ud4-trial

# redeploy the k8s cluster services with new images
# cd ~/git/udcn_course4/Project_Starter_Files-Building_a_Metrics_Dashboard/manifests
# kubectl apply -f app/

# delete pods to force re-pull of new images
# kubectl rollout restart deploy frontend
# kubectl rollout restart deploy backend