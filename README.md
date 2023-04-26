# AutoTruck - Yard Automation Demonstration. 

The AutoTruck was a project that aimed the automation of logistic centers.

Its implementation was accomplished through the use of the [helyOS framework](https://helyos-manual.readthedocs.io/en/latest/) and the TruckTrix&reg; path planner.<br>

Here, we have prepared this demo version to run the application in your own computer with the aid of [Docker](https://www.docker.com/) containers.
For this local version, the TruckTrix&reg; service was substituted by a simple clothoid path planner.

 ## Core features
  * Click in the map for the final destination to drive.
  * Use online TruckTrix&reg; path planner service to plan collision-free paths. (*)
  * Alternatively, use local path planner to plan clothoid paths.
  * helyOS is employed to integrate AutoTruck web app, path planners, message broker and the vehicle simulator.
  * Create different types of missions (must be registered in helyOS dashboard).

(*) See details below in [Setting TruckTrix as path planner](#setting-trucktrix-as-path-planner).



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

 ## To restart vehicle simulator
```
 docker-compose restart  agent_simulator
 ```

 ## To restart application

```
docker-compose down -v
docker-compose up
```
The (-v) will delete the database.

</br>
</br>



# Exploring the helyOS backend

The AutoTruck app uses helyOS as backend.  You can access the helyOS dasboard to configure the backend.


## helyOS Dasboard

[http://localhost:8080/](http://localhost:8080/)

*username*: admin

*password*: admin

<br>


## Setting TruckTrix as path planner

TruckTrix&reg; is a robust multi-joint path planner developed by Fraunhofer IVI. </br> 

The choice of which path planner is used by the application can be set up in helyOS dashboard. 
So you can choose the AutoTruck app to use the online TruckTrix path planer or the local clothoid path planner.

To utilize TruckTrix,  it is necessary to request an API-key from Fraunhofer IVI ( trucktrix [at] ivi . fraunhofer . de ).

The API-key must be added in `settings/licenses/service_licenses.ini` or saved in the *trucktrix* API-key field in http://localhost:8080/dashboard/#/all-services.

In the helyOS dashboard `Microservices` view, disable the local_path_planner and enable the TruckTrix service.

<br>

## Yard and Missions Data
Using the GraphQL language, you can programmatically access the complete yard data stored in the helyOS database.

[http://localhost:5000/graphiql](http://localhost:5000/graphiql)
 



## Contact
helyos [at] fraunhofer . ivi . de (without spaces)


<!-- ## Production
<img src="image/Docker_architeture.png" alt="drawing" width="800"/>



## Development
<img src="image/Devarch.png" alt="drawing" width="800"/> -->