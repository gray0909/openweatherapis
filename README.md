# Weather API using GraphQL and Django


##Considerations
- due to limitation of free openweather API using loop to fetch data for each city
- limited number of default cities which would ideally be replaced with an ETL system to bulk download weather data, load static city data and other metadata(weather condition, etc)

##Starting up

1. Make sure python version 3.6+
2. Create and activate virtual env
3. initial load of data through command:
```bash
 python manage.py loaddata db.json
```
4. use url -> http://localhost:8000/graphql
5. provide query

visitsCity eg:
```
query {
  visitsCity(weatherCon: "rain", cityList: ["Beijing", "Barcelona", "Toronto", "Bangkok"], dayDiff: 1) {
    id
    name
    long
    lat
  }
}
```

hottestCity eg:
```
query {
  hottestCity(cityList: ["Beijing", "Barcelona", "Toronto", "Bangkok"], dayDiff: 1) {
    id
    name
    long
    lat
  }
}
```
