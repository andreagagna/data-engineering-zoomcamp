### Introduction to Docker Basic Commands

1. **hello-world**
   - Description: This command runs a simple container that prints a "Hello World" message. It's often used to test if Docker is properly installed and working.

   ```bash
   docker run hello-world
   ```

2. **Run ubuntu 20.04**
   - Description: This command runs an interactive Ubuntu 20.04 container.

   ```bash
   docker run -it ubuntu:20.04
   ```

3. **Run python 3.9 interactively**
   - Description: This command runs an interactive Python 3.9 container.

   ```bash
   docker run -it python:3.9
   ```

4. **Run python 3.9 interactively with bash entrypoint**
   - Description: This command runs an interactive Python 3.9 container with a bash entry point.

   ```bash
   docker run -it --entrypoint=bash python:3.9
   ```

5. **Build the docker image in the current directory and tag it to name=test and tag=pandas**
   - Description: This command builds a Docker image from the current directory and tags it with the names "test" and "pandas".

   ```bash
   docker build -t test:pandas .
   ```

6. **Run the previous built docker image interactively with a date argument**
   - Description: This command runs the previously built Docker image interactively and passes a date argument.

   ```bash
   docker run -it test:pandas date
   ```

These commands cover basic Docker operations, including running containers interactively, building images, and executing commands within containers.