## Run LocalJobs Application on OpenShift##

1. Create OpenShift Python 2.7 application with MongoDB database     
```
$ rhc app create localjobs python-2.7 mongodb-2.2
```
2. Pull the source code from git repository
```
$ cd localjobs
$ git remote add upstream -m master https://github.com/shekhargulati/localjobs-python2.7.git
$ git pull -s recursive -X theirs upstream master
```

3. Import the data into MongoDB database
```
$ rhc show-app
$ scp jobs-data.json <ssh url>:app-root/data
$ rhc ssh
$ cd app-root/data
$ mongoimport -d localjobs -c jobs --file jobs-data.json -u $OPENSHIFT_MONGODB_DB_USERNAME -p $OPENSHIFT_MONGODB_DB_PASSWORD -h $OPENSHIFT_MONGODB_DB_HOST -port $OPENSHIFT_MONGODB_DB_PORT
```
4. Push the code to application gear
```
$ git push
```

5. Application will running at http://localjobs-{domain-name}.rhcloud.com. Please replace {domain-name} with your own domain name.
