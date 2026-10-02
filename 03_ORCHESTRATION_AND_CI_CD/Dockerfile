FROM alpine:3.20

RUN apk add --no-cache python3 py3-pip ca-certificates &&     addgroup -S swainjohn && adduser -S -G swainjohn swainjohn &&     mkdir -p /app /var/lib/swainjohn &&     chown -R swainjohn:swainjohn /app /var/lib/swainjohn

WORKDIR /app
COPY . /app

USER swainjohn
CMD ["python3", "-m", "http.server", "8080"]
