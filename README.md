# AutoTruck - yard automation demonstration. 

The AutoTruck is a demo application for automation of logistic centers.

This project was successfuly implemented by using the helyOS framework. </br> 
We have prepared this local deployment that allows you to run  the application in your computer with the help of [Docker](https://www.docker.com/).


 ## Core features
  * Use local path planner to plan paths.
  * Use online TruckTrix&reg; path planner service to plan free colision paths. (*)
  * Automatic registration of vehicle (agent) via RabbitMQ message broker.
  * Assignment of user-triggered processes to one or several services for path calculation (configurable using helyOS dashboard).
  * Collection of path calculations via dashboard 


(*) TruckTrix&reg; is a powerful path planner. You need to request the TruckTrix API-key from Fraunhofer IVI. </br> 
The API-key must be added in `settings/licenses/service_licenses.ini`.

</br>
</br>

 ## To start
 
```
docker-compose up -d
```

</br>

## Open the application

* Autotruck-Trucktrix (it will automatically connect to helyOS)

[http://localhost:3080](http://localhost:3080/)

*username*: admin

*password*: admin

</br>

 ## To restart

```
docker-compose down -v
docker-compose up
```
The (-v) will delete the database.

</br>
</br>



# Exploring the helyOS backend

Use helyOS dasboard to configure the backend.


## helyOS Dasboard

[http://localhost:8080/](http://localhost:8080/)

*username*: admin

*password*: admin


You can also insert the TruckTrix API-key in the `Microservices` view.

<br>

## GraphiQL
Explore the helyOS database using the GraphQL language.

[http://localhost:5000/graphiql](http://localhost:5000/graphiql)
 






<!-- ## Production
<img src="image/Docker_architeture.png" alt="drawing" width="800"/>



## Development
<img src="image/Devarch.png" alt="drawing" width="800"/> -->