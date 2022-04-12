echo "1. easy get json : curl localhost:8000/info"
curl localhost:8000/info -w '\n\n'

echo "2. easy post data : curl --data 'num=15' localhost:8000/info"
curl --data "num=15" localhost:8000/info -w '\n\n'

echo "3. GET time : curl localhost:8000/time"
curl localhost:8000/time -w '\n\n'

echo "4. using gevent to finish crawler IO-bound task : curl localhost:8000/crawler"
curl localhost:8000/crawler -w '\n\n'

#curl localhost:8000/download -w '\n\n'
echo "5. using gevent to finish CPU-bound task : curl localhost:8000/factorial/8"
curl localhost:8000/factorial/8 -w '\n\n'
