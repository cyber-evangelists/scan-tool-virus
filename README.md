
# Virus Scanner

## Overview
This project is a web backend built using Python and FastAPI, featuring RESTful APIs and fully dockerized with MongoDB integration. It specializes in two core functionalities:
- **File Scanning:** Analyzes files to detect potential threats using various antivirus tools.
- **URL Scanning:** Examines URLs for suspicious activities, reporting findings based on multiple antivirus checks.

## Features
- RESTful API endpoints for file and URL scanning.
- Dockerized environment including MongoDB.
- Real-time analysis and reporting of potential threats.

## Getting Started

### Prerequisites
- Docker Desktop Application
- Docker Compose

### Installation
Clone the repository:
```bash
git clone [Your Repository URL]
cd [Your Project Directory]
```

### Running the Application with Docker Compose
Use Docker Compose to set up and run the application:
```bash
docker-compose up --build
```
This command will build the Docker images and start the containers as defined in your `docker-compose.yml`.

### Accessing the Application
- The FastAPI backend will be available at `http://localhost:9000`.
- For API documentation and testing, Swagger UI can be accessed at `http://localhost:9000/docs`.

