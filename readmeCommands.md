# Bread Van App - CLI Commands Reference

A comprehensive command-line interface for managing bread delivery operations with drivers, residents, and route assignments.

## Table of Contents
- [Setup](#setup)
- [User Commands](#user-commands)
- [Route Commands](#route-commands)
- [Driver Commands](#driver-commands)
- [Resident Commands](#resident-commands)


## Setup


### Setup and activate virtual environment to run python 3.9.10
#### Had to do it becuase of multiple python versions due to the course big data

```bash
python -m venv venv
```
```bash
.\venv\Scripts\activate
```


### Initialize the Database
```bash
flask init
```
This command creates the database and populates it with:
- 6 street routes (Maple Street, Oak Avenue, Pine Lane, Cedar Road, Birch Boulevard, Ash Drive)
- 5 drivers with unique IDs
- 10 residents with unique IDs distributed across different streets

## User Commands

### List All Users
```bash
flask user list 
```

## Route Commands

### List All Routes
```bash
flask route list
```
- Displays all available delivery routes with route IDs and street names


## Driver Commands

### Select Route for Driver
```bash
flask driver select-route <driver_id>
```
- **driver_id**: Integer ID of the driver
- Allows drivers to choose their delivery route
- Automatically sets driver status to "Active" upon route assignment

**Example:**
```bash
flask driver select-route 1
```

### Toggle Driver Status
```bash
flask driver status <driver_id>
```
- **driver_id**: Integer ID of the driver
- Toggles driver between Active and Inactive status
- Shows current route if active

**Example:**
```bash
flask driver status 1
```


## Resident Commands

### View Resident Inbox

```bash
flask resident inbox <resident_id>
```
- **resident_id**: Integer ID of the resident
- Shows scheduled delivery drivers for the particular resident's street

**Example:**
```bash
flask resident inbox 1
```

### Request Delivery Stop
```bash
flask resident request-stop <resident_id> <driver_id>
```
- **resident_id**: Integer ID of the resident
- **driver_id**: Integer ID of the driver
- Allows residents to request a stop from the driver (their order and delivery instructions)


**Example:**
```bash
flask resident request-stop 1 2
```

### Track Driver Location
```bash
flask resident track-driver <resident_id> [driver_id]
```
- **resident_id**: Integer ID of the resident
- **driver_id**: - Without driver_id: shows all drivers on resident's street
                 - With driver_id: shows specific driver's status and location

**Examples:**
```bash
flask resident track-driver 1        # Track all drivers on street
flask resident track-driver 1 2      # Track specific driver
```



## Quick Start Guide

### 1. Initialize System
```bash
flask init
```

### 2. View Available Resources
```bash
#view data
flask user list      
flask route list       
```

### 3. Assign Driver to Route
```bash
flask driver select-route 1
# Follow prompts to select route
```

### 4. Check Resident Inbox
```bash
flask resident inbox 1
# See assigned drivers for resident's street
```

### 5. Request Delivery
```bash
flask resident request-stop 1 1
# Resident 1 requests delivery from Driver 1
```

### 6. Track Driver
```bash
flask resident track-driver 1 1
# Track Driver 1's location and status
```

