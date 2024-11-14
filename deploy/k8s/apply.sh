# apply each manifest in the directory


for file in $(ls *.yaml); do
  kubectl apply -f $file
done