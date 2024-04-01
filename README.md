# Deploy BE
```
docker build -t patch-em-all-be .
docker run -d --rm --name patch-em-all-be -p 3000:3000 -e AUTH_SECRET=<SECRET>> patch-em-all-be
```

# Deploy FE
```
docker build -t patch-em-all-fe .
docker run -d --rm --name patch-em-all-fe -p 80:80 patch-em-all-fe
```