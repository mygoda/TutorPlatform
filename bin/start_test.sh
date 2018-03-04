
echo "docker-compose down"
/usr/local/bin/docker-compose -f docker-compose_test.yml down

echo "docker-compose up"
/usr/local/bin/docker-compose -f docker-compose_test.yml up -d