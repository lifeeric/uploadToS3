# Move files to S3

First of all, you have to install the `boto3` and `threading` if you don't have in the system.


#### Optional
if you wanna create virtual env
```bash
$ python3 -m venv env
$ source env/bin/activate
```


#### install 

```bash
$ pip install boto3
```

#### run
you have pass the directory path as flag (argument) to the script and it will get all files from directory & will upload it to S3.
```bash
$ python index.py <directory path>
$ python index.py ./files
```

## Command 
run this command in the directory where has the sub-directories with files
```bash
$ for d in */*/*; do uploadToS3 $d; done;
```

##### checking logs
change dir to `/home/centos/logs` and run, if you see empty array, no error else problem.
```bash
$ for f in *; do echo $f; echo " == "; cat "$f"; done
```


##### Watcher
it watches for a files in directory, if new file are created it so upload it to s3
```bash
inotifywait -m -r -e create testDir/ | while read DIRECTORY EVENT FILE; do   
	case $EVENT in CREATE*)         
		for d in testDir/*/*; do uploadToS3 $d; done;            
		;;    
	esac; 
done

```


[@lifeeric](https://github.com/lifeeric)