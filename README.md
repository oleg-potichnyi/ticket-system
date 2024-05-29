# Ticket system

This is a simple ticket system web application built with Flask that implements role-based access control (RBAC) for different user roles (Admin, Manager, Analyst) and user groups (Customer 1, Customer 2, Customer 3).

## Features

* User Authentication
* Role-Based Access Control (RBAC)
* Ticket Management
* Group Management
* User Interface

## Technology stack

* Backend:
  - Language: Python 3 
  - Framework: Flask 
  - Database: SQLite 
* Frontend
  - HTML/CSS
* Dependency Management: pip
* Virtual Environment: venv
* Database Migrations: Flask-Migrate
* Collaboration and Version Control:
  - Version Control System: Git
  - Repository Hosting: GitHub
* Containerization platform
  - Docker
* Other: requirements.txt

## Installation

### Prerequisites

  - Python 3.x
  - Docker
  - Docker Compose

### Setup

* Clone the repository
```shell
  git clone https://github.com/oleg-potichnyi/ticket-system
  cd ticket-system
```

* Build and run the Docker container
```shell
  docker-compose up --build
```

* Run database migrations
```shell
  docker-compose exec web flask db upgrade
```

 * Access the application
```shell
  Open your web browser and go to http://localhost:5000
```
