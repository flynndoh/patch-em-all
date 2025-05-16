# Deploy BE
```
docker build -t patch-em-all-be .
docker run -d --rm --name patch-em-all-be -p 3030:3030 -e AUTH_SECRET=<SECRET>> patch-em-all-be
```

# Deploy FE
```
docker build -t patch-em-all-fe .
docker run -d --rm --name patch-em-all-fe -p 8080:8080 patch-em-all-fe
```