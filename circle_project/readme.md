# Line Server

This is a python/django implementation of "`line server problem`".

## Build & Run

1. Make sure you have `pip` installed on your system.
2. `Clone` the whole project to your local.
3. Go to the `circle_project` directory which has `build.sh` & `run.sh`.
4. Run `build.sh` to create a virtualenv and install packages specified in `requirements.txt`.
5. Run `run.sh` to start your local server. 
	* app root: <http://127.0.0.1:8000/line_server/>
	* get lines: <http://127.0.0.1:8000/line_server/lines/1/>
	
## Questions

### How does your system work?

There are different approaches to solve this problem. From easy to advanced solutions:

1. When the file size < 1Gb, and there are not too many requirements(**uptime**, **server failure**, etc), it's feasible to just read all lines to a local array. The index of the array will represent the line number.  
	* pros: easy and feasible.
	* cons: The modern web application should be stateless, which is good for **_scalability_** and **_robust_**. When the server is down(loal variable will be gone), or need to serve bigger file, this approach will not meet the needs.
	
2. When the file is really big(1G ~ 100G), we can preprocess the file and divide the single big file to separate smaller files with fixed number of lines. We can use an in-memory dict/hashtable to store the filename-line_range mapping.
	* pros: a single server can handle a really big file.
	* cons: still need to find lines in any smaller file chunck.
	* improvements: 
		* To prevent from disk failures, we can store the smaller file chucks to multiple server disk/SSD (for replica), or/and to cloud storage like S3. Also update the in-memory dict to store the node ip address.
		* Move the local in-memory dict mapping to any clustered in-memory db, like redis or aerospike. 
		
3. Consider using DB technologies. The essence of this problem is similiar to db lookup: How can we improve the retrieve performance for a certain row in a large table? The column index is invented to solve this problem by creating a self balanced tree for speedup. Also db is ideal for high availablity & high scalability. 

	So in my project, I preprocess the file and store the line number and line content data in a SQlite database. And created an index on column line_num to speedup the row retrieval. Using sqlite is just a demo, since backed db can be any kinds, like mysql, postgres, or even NoSQL.
	* pros: use exsited technology(index, great availability & scalability) to solve our problem.
	* cons: no obvious points. maybe more configurations and setup.
	* improvements: 
		* When file size is around 10Gb level, it's also feasible to use in-memory db to store all data including index in memory.
		* Since the file is plain text with all ascii, exsited compress algorithm(like gzip) is pretty good at compressing text. In average, after compression the file size will be 1/3 of the orignal one. So even consider 100Gb file, it's only around 40GB after compression. And modern RAM size of a single node can reach ~100Gb, which means, one redis node or a redis cluster with 2 nodes is good enough to load all data in memory.
		
4. As described in above improvements, a single redis node or a cluster of 2 is good enough to serve 100GB file. Any other options, including aerospike, are even better. Aerospike can store index in memory while store data in SSD, this reduce the expenses of RAM. Also when add nodes to aerospike cluster, it can dynymically balance the node data distribute and access load.

### What do we need to build your system?

Since python is a dynamic script langauge, there is no need to build/compile. In the actual `build.sh`, just install any required packages.

### How will your system perform with a 1 GB file? a 10 GB file? a 100 GB file?

Different approaches will handle the file quite differently, like described above. 

### How will your system perform with 100 users? 10000 users? 1000000 users?

The bottlenecks for high QPS mainly exist in 2 places: 

1. The python application server. In real prod situation, we use Gunicorn with ~10 workers to serve python application. A single Gunicorn server can handle 100 QPS easily. Since in the question, the access load of 100, 10k or 1000k users may distribute evenly in a day. Consider 100 QPS, this equals to 100 * 60 * 60= 360k, which means with a single gunicorn server, it can handle 360k users in an hour. With more traffic, we can just add more gunicorn nodes after a load balance, like nginx. The 3 nodes can handle 1000k users.

2. IO servers. First, we can have more replicas to server the  data(since there is only read action in io server, we have no problem of replica data sync); Then, we can use in-memory db to serve the data.

For extreme high QPS situation, there is another solution to solve the problem. As we know, nginx is really good at serving static data. Considering our file is also immutable, we can let the nignx serve it directly.

There is project called `OpenResty`. We can write lua script to control our business logic inside the nginx. Also there is an OpenResty lua MVC web framework called `vanilla`. We can use vanilla to write any business logic and even read data from redis. Which means, we removed the python application server layer and read data directly from memory.

### What documentation, websites, papers, etc did you consult in doing this assignment?

* django <https://www.djangoproject.com/>
* aerospike <http://www.aerospike.com/>
* plain text compress ratio <https://binfalse.de/2011/04/04/comparison-of-compression/>
* openresty <https://openresty.org/en/>
* vanilla <https://github.com/idevz/vanilla>

### What third-party libraries or other tools does the system use? How did you choose each library or framework you used?

I use django to build the api. Even though it seems a little heavy to complete a small task using django, it's fast to have a working version, considering my django background.

### How long did you spend on this exercise? If you had unlimited more time to spend on this, how would you spend it and how would you prioritize each item?

It takes me 1 hour to figure out different approaches, 1.5 hour to write the code, 2 hour to summarize my thought to documents.

If I have more time, I may setup a redis instance and try to serve the data from memory. (In fact, django can also serve the sqlite from memory, with few configs update.)

### If you were to critique your code, what would you have to say about it?

I have tried to optimize my current code to an ideal level, including django bulk objects creation, batch saving every certian lines of text, etc.





 



	


