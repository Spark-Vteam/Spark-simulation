# Spark simulation

This is a submodule of the Spark Project.

The spark simulation is a larger test suite for the project as a unit. It consists of one modified bike object in order to reduce stress on hardware. It simulates a realistic flow of user traffic with registered users unlocking bikes, riding at realistic and randomly generated routes. After the destination is reached the rent is finished by creating an invoice and leaving the bike available for someone else to use, unless it runs out of battery.

You will also notice hove the bikes interact with geofenced areas and the speed will be affected if the zone is a slow or forbidden zone. The simulated will also not be able to park in a forbidden or no parking zone, instead they will turn around and try to find an allowed zone. If they finish a trip in a parking zone it will show on the bike status and generated invoice.

Since the simulation is a API you will find a set of controls to manipulate the simulation below.

It depends on the Database, Client Server and Bike Server to be up and running.

## Start the simulation

The Simulation service can be started with

```bash
# First time using
docker compose build

# Start the service in detached mode
docker compose -d up flask-server
```

## Interact with the simulation

To interact with the features of the Simulation you have these routes at your disposal.

```python
# Listening at localhost:8000


# Start the activation of bikes
GET /sim_start

# Stop the activation of bikes
GET /sim_stop

# Activate a specific bike to ride a specific route
GET /activate/<bike_id>/<user_id>/<position>/<destination>

# Stop a specific bike
GET /stop/<bike_id>
```

## Performance issues

The simulation is simulating close to 4000 users and 4000 bikes in three major cities of sweden and in order to actually test the systems durability and not just give a pleasant visual element, the application is bound to get heavy.

Every few seconds all bikes are iterated with a set chance to becoma active and start riding a specific route. A user is connected to the bike and a rent is created. Every few seconds all active bikes are also iterated in order to update the database with its latest details through the bike server. All while checking battery status, geofence interactions and much more.

When creating the simulation object, you are given a few optinal parameters in order to increase performance.

```python
# Create a default simulation
Sim = Simulation()

# Increase the time between iterations
Sim = Simulation(emit_frequency=10) # Defaults to 5

# Lower the chance of a bike to get activated
Sim = Simulation(activation_chance=0.005) # Defaults to 0.01
```

