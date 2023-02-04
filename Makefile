image: 
	docker build -t pyredis .

run:
	docker run -it -p 8080:8080 pyredis

test:
	pytest -v