# Fonteyn Customer Website & API

## Project Overview

An educational group project developed during the HBO-ICT
programme at Fontys University of Applied Sciences.

The project focuses on developing a customer-facing web
application with a separate backend API, database integration,
authentication, containerization and CI/CD automation.

## Key Features

### Customer Website
- Customer registration and login.
- Customer profile pages.
- Booking functionality.
- Payment-related functionality.
- Frontend and backend communication.
- Web interfaces using HTML, CSS and JavaScript.

### Backend API
- Python-based backend application.
- Modular API architecture using Flask Blueprints.
- Authentication and user management.
- Database models and integration.
- Payment-related API endpoints.

### Security
- User authentication.
- Password hashing.
- Environment-based configuration.
- Separation of frontend, backend and database services.

### Infrastructure & DevOps
- Docker containerization.
- Multi-container configuration using Docker Compose.
- Nginx web server configuration.
- Azure DevOps CI/CD pipelines.
- Version control and collaborative development.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Flask | Web application and API development |
| HTML | Website structure |
| CSS | Website styling |
| JavaScript | Frontend functionality |
| SQL | Database management |
| Docker | Containerization |
| Docker Compose | Multi-container infrastructure |
| Nginx | Web server configuration |
| Azure DevOps | CI/CD automation |
| Git | Version control |

## Project Structure

    .
    ├── Customer API/
    │   ├── blueprints/
    │   ├── app.py
    │   ├── models.py
    │   ├── requirements.txt
    │   └── Dockerfile
    ├── Customer Website/
    │   ├── blueprints/
    │   ├── static/
    │   ├── templates/
    │   ├── app.py
    │   └── Dockerfile
    ├── database/
    │   └── schema.sql
    ├── Nginx/
    ├── docker-compose.yml
    ├── azure-pipelines.yml
    ├── azure-pipelines-cicd.yml
    └── README.md

## Learning Objectives

- Full-stack application development.
- Backend API development and integration.
- Authentication and password security.
- Relational database management.
- Docker containerization.
- Web server configuration.
- CI/CD pipeline development.
- Technical troubleshooting.
- Collaborative software development.

## Project Status

This repository is an educational group project preserved
for portfolio and learning purposes.

Some functionality may be incomplete or require additional
configuration. The application is not intended for
production use.

Sensitive environment configuration files are excluded
from this repository.

## Future Improvements

- Improve authentication and authorization.
- Implement additional input validation.
- Expand automated testing.
- Improve error handling and logging.
- Implement automated security scanning.
- Improve deployment documentation.

## Contributors

Developed collaboratively during the HBO-ICT programme
at Fontys University of Applied Sciences.
