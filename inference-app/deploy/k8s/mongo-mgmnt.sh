# Connect to MongoDB shell from test pod
kubectl exec -it kafka-client -- mongosh mongodb://mongodb:27017/

# Basic MongoDB commands to run inside the shell
```bash
# List databases
show dbs

# Switch to database
use team5_vm3_db

# List collections
show collections

# Query documents
db.images.find()

# Pretty print results
db.images.find().pretty()

# Count documents
db.images.countDocuments()