curl https://query.yahooapis.com/v1/public/yql \
   -d q="select * from weather.forecast where woeid=2151849" \
   -d format=json
