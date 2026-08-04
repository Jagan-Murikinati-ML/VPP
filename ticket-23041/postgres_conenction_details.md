these asset db is in azure, its a postres database, i will conenct like this
1) open wsl, and execute curl ifconfig.me, to find out my ip and set configure this ip in configure networking section in azure 
2) after that will execute psql "host=assetregistry-us-es-dev-postgre.postgres.database.azure.com port=5432 dbname=assetdb user=esadmin sslmode=require", i set the password and execute that, 