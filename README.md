# Running a nginx docker container using terraform

<br/>

### Installing Terraform in window's machine
---

- Download Terraform - <https://www.terraform.io/downloads> `Amd64 file`
- Unzip the downloaded file and move the exe file to C drive `<C:\terraform>`
- Set the terraform binary application file to the enviromental variable path
- Verify the installation `terraform -help`


### Running nginx container

` First install docker desktop in your windows maching `

### Steps:

- Create a directory named `terraform-docker-container`
   `mkdir terraform-docker-container`
- Navigate to the created folder 
    `cd terraform-docker-container`
- Now, create a file `main.tf` and paste the following code

```ts

terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = ">= 2.13.0"
    }
  }
}

provider "docker" {
  host    = "npipe:////.//pipe//docker_engine"
}

resource "docker_image" "nginx" {
  name         = "nginx:latest"
  keep_locally = false
}

resource "docker_container" "nginx" {
  image = docker_image.nginx.latest
  name  = "tutorial"
  ports {
    internal = 80
    external = 8000
  }
}
```

- Initialize the project, which downloads a plugin that allows Terraform to interact with Docker `terraform init`

```powershell
 $ terraform init 
```
  
- Provision the `NGINX` server container with apply. When Terraform asks you to confirm type `yes` and press `ENTER`.  `terraform apply`

```powershell
 $ terraform apply 
```
  
- Verify the existence of the `NGINX` container by visiting <http://localhost:8000> in your web browser or running docker ps to see the container.

```powershell
 $ docker ps 
```

- To stop the container, run terraform destroy `terraform destroy`

```powershell
 $ terraform destroy
```


