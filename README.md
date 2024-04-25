# Overview

Advanced Docker exercises covering:

- using minimal docker images to run workloads
- multi-stage dockerfiles
- running as non root user
- using docker compose to run microservices

## Flow - Exercises overview - trainer version

- First exercise is to show how big the python base image is
- Introduce Alpine - they'll need to write the appropriate commands in the dockerfile to install python and pip and run `api.py`
  - There will be issues running pip and installing packages globally, they'll need to come up with solutions to this. They need to read the error messages carefully, it will give them the solution uptions!
- Introduce the Alpine base image with python installed, then same exercise to bbuild a dockerfile to run the `api.py`
- Introduce the concept of a multistage dockerfile where we can use a build stage and a production stage.
  - The exercise is for them to try and right a multi-stage pipeline, the first stage will install pip and do the build, the second stage will copy the built files and simply run them (no pip needed)
  - The exercise should be introduced explaining that for the production stage, because we're not installing deps using pip we'll need to think about how to tell the runtime where the uvicorn executable is, we get this PATH update for free when running pip, but our production stage won't have this.
- The key point with these three exercises is to highlight the differences in size between opting for a minimal distribution (like Alpine) as against a fully blown package like the Python base image. For production workloads we want to minimise container foot print, why? Because we better exploit the benefits of containers which should provide the smallest foot print of O/S software needed to run our workloads. In other words: don't install more than we need.
- The next exercise is security based: th essence is: Don't run containers as the root user. So we'll need to do some priming on bash calls such as `adduser` and `chown` and briefly discuss how the file permissions work in Linux: assign permissions to a user, group and then everybody else.
  - The exercise is to augment the multi-stage pipeline with additional `RUN` directives in order to create the user, assign permissions and `USER` directive to set the user.
- The final exercise is intended to demonstrate the capability of `docker compose` a cosmosdb is needed to get this to work (don't use the emulator as it enforces ssl which doesn't work in windows on docker because of a hostname issue).
  - It's like this makes more sense as a demonstration of how to use docker compose, but a suggested exercise might be for them to read the src code and create a new microservice for say, employees and then add a new entry into the docker compose file for that service to build and run it as as container in the compose environment
  - There are two microservices in the `src` folder which have an associated docker file each. The company and department services.
  - They create their own containers and data from a static array in `data.py` within a cosmosdb.
  - The `compose.yaml` file contrains the instructions to build and run the two microservices in containers, just run `docker compose up`. Then you can access the apis using `http://localhost:<port number from compose.yaml>/docs`.
  - The employees service could be created by adding employee data to the array in `data.py` per department array and then using the existing services as a template to create a new one with an endpoint to get employees per company and department as an example. Create a dockerfile for the new service (using the existing ones as a template) and finally create an entry in the `compose.yaml` file to build and run the container for it.

## To get the microservices working

- You'll need to create a cosmosdb instance in Azure (throughout based, not serverless).
- Create a .env file at the root of the repo and add two environment variables to it:
  - COSMOSDB_ENDPOINT_URL
  - COSMOSDB_MASTER_KEY
- Grab these details from Azure Portal (open the cosmosdb you created and look in the `keys` section)
- The microservices provision their own database and containers.

## Exercises

- Taking Alpine as the base image, write  dockerfile that will build an image that runs the fastAIP in `api.py` code. Hints:
  - Alpine doesn't have `pip` or `python` installed, write the appropriate statements in your dockerfile to install these tools.
  - Read error messages carefully! They will often include options to recitfy your problem
  - Note the size of the image that you create
- Now see if you can find a distribution of Alpine that already has python and pip installed and develop your dockerfile as above.
  - Compare the size of your container image to the previous exercise.
- Now construct a multi-stage docker file. The first stage will build your code using whatever base image you like. The second needs to use as smaller image as possible and should only include bare minimum needed to run the fastAPI
  - Note that to keep your production stage as minimal as possible you ideally should install pip, so you will need to find another approach to getting the dependencies that the fastAPI needs, onto your container and subsequently updating the PATH so that, for example you can execute the `uvicorn` command.
- Adapt your production stage in your docker file to run the container as a non root user. Hint:
  - You will need to create the user and also assign ownership to that user (using the correct commands for your chosen base image distribution) to the correct directory on your container in order for it to run the code.
- Compose exercise, using the company and department service as examples add a third microservice for employees in each department and then udpate to the docker compose file to run this microservice locally with the others.
