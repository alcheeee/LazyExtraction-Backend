# Lazy Extraction API

A REST API for a simple extraction-shooter game, built with [FastAPI](https://github.com/fastapi/fastapi). The API uses SQLModel and a PostgreSQL database for user data. Some of the functionality includes weapon customization, inventory management, attachment management, and stat tracking. Much of it is early in development.

## Stack

- **Framework**: [FastAPI](https://github.com/fastapi/fastapi)
- **Database**: PostgreSQL, Redis(cache) - not integrated, but ready
- **ORM**: SQLModel, SQLAlchemy
- **Testing**: [Testcontainers](https://github.com/testcontainers/testcontainers-python), [pytest](https://github.com/pytest-dev/pytest), unittest
- **Containerization**: Docker
- **Frontend Integration**: The API is designed to integrate with any frontend, though I'm creating the frontend with Godot 4 (*will be released soon*)
- **Poetry**: This will come in the next update.

## Features

- **Inventory Management**:
  - An Inventory and Stash.
  - Equippable items, Clothing, Armor and Weapons
  - Quantity tracking with error handling for invalid states.
  
- **Weapon Customization**:
  - A detailed weapon modification system, supporting multiple attachments like Foregrips, Muzzles, Magazines, Stocks, Scopes, and Handgaurds.
  - Attachment items dynamically affect weapon stats.
  - Efficiently maintains the correct quantity of attachments based on added/remove attachments.

- **Market System**:
  - A dynamic market where players can buy and sell items.
  - Customizated weapons carry their modifications through transactions.

- **Randomized World Generation**:
  - Fully integrated [Loot Tables](/backend/app/game_systems/game_world/room_drop_data.py)
  - Saves world data in a JSONB column.
  - The ability to traverse rooms (Generate a new room when already in one).
  - Randomly generated items that are able to be picked up.
  - Minimum amount of "Actions", such as traversing and picking an item up, before being allowed to extract.

- **Player Crews**:
  - Players can create crews, 
  - Leaders can remove crew members, and add crew members
  - Many features and checks are missing here. 
    - A Leader can choose anyone to add (so long as they aren't in another crew), and they will be added to that crew without accepting.
    - Leaders cannot delete crews
  - This feature is not a priority, other areas need improvement.

- **Player Data Management**:
  - Password Hashing with Argon2
  - JWT-Token Authentication with Access and Refresh tokens

- **Testing**:
  - Unit tests to validate code across the API.
  - Mocking database interaction in tests for efficient and isolated API testing.
  - Database CRUD tests


## Running the API locally

> [!NOTE]
> Make sure [Docker](https://www.docker.com/) is installed and running on your system.


1. **Clone the repository**:

   ```bash
   git clone https://github.com/alcheeee/LazyExtraction-Backend.git
   cd LazyExtraction-Backend
   ```

2. **Set up the environment**:

   Create a docker network for the API to communicate with the database.
   If you want to have the database container hosted seperate from the server container, you will need this to have the two containers communicate.

   ```bash
   docker network create lazy_api_network
   ```

2.5. **Configure environment variables**:

   Create a `.env` file using the [.env-example](.env-example) file within the project.
   For this example, we'll just rename the `.env-example` file to `.env`.
   Note that changing certain variables may require they be changed in the [database-compose.db.yaml](database/docker-compose.db.yaml) file and the [docker-compose.app.yaml](docker-compose.app.yaml) file.

3. **Database setup**:

   Create the database Docker container.

   ```bash
   cd database
   docker-compose --env-file ../.env -f docker-compose.db.yaml up -d
   ```

4. **Build the API Docker container**:

   Migrate the database schema using Alembic (if applicable):

   ```bash
   cd ..
   docker-compose -f docker-compose.app.yaml up --build
   ```

5. **Enjoy**:

   Once the server is done setting up, the API documentation can be accessed at [http://localhost:8000/docs](http://localhost:8000/docs).

## Testing

Unit tests are provided to ensure functionality across the application. To run the tests:
(some are broken due to some JSON structure changes right now, can be fixed quickly)

```bash
pytest app/tests/unit_tests/ -v -rP
```

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the [LICENSE](LICENSE) file for details.
