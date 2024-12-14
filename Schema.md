## Database Schema

### `race` Table
This table stores information about each race, including its details such as location, date, and conditions.

| Column Name      | Data Type    | Key Type           | Description                     |
|------------------|--------------|--------------------|---------------------------------|
| id               | TEXT         | Primary Key        | Unique identifier for the race |
| race_number      | INTEGER      |                    | Number of the race             |
| race_name        | TEXT         |                    | Name of the race               |
| race_date        | TEXT         |                    | Date of the race               |
| race_time        | TEXT         |                    | Time of the race               |
| type             | TEXT         |                    | Type of the race               |
| length           | INTEGER      |                    | Distance of the race in meters |
| length_class     | TEXT         |                    | Classification by race length  |
| handed           | TEXT         |                    | Direction of the race course   |
| weather          | TEXT         |                    | Weather during the race        |
| condition        | TEXT         |                    | Track condition                |
| place            | TEXT         |                    | Location of the race           |
| course           | TEXT         |                    | Type of course (e.g., turf)    |
| round            | INTEGER      |                    | Round number                   |
| days             | INTEGER      |                    | Day of the racing event        |
| head_count       | INTEGER      |                    | Number of participating horses |
| max_prize        | REAL         |                    | Maximum prize money for the race |

**Foreign Keys:**
- `id` = `entry.race_id`
- `id` = `result.race_id`
- `id` = `history.race_id` (conditional: `history.horse_id` used)

---

### `horse` Table
This table contains information about each horse, including its ancestry details.

| Column Name      | Data Type    | Key Type           | Description                     |
|------------------|--------------|--------------------|---------------------------------|
| id               | TEXT         | Primary Key        | Unique identifier for the horse |
| father_id        | TEXT         |                    | Identifier for the father horse |
| father_name      | TEXT         |                    | Name of the father horse        |
| mother_id        | TEXT         |                    | Identifier for the mother horse |
| mother_name      | TEXT         |                    | Name of the mother horse        |
| f_father_id      | TEXT         |                    | Identifier for paternal grandfather |
| f_father_name    | TEXT         |                    | Name of paternal grandfather    |
| f_mother_id      | TEXT         |                    | Identifier for paternal grandmother |
| f_mother_name    | TEXT         |                    | Name of paternal grandmother    |
| m_father_id      | TEXT         |                    | Identifier for maternal grandfather |
| m_father_name    | TEXT         |                    | Name of maternal grandfather    |
| m_mother_id      | TEXT         |                    | Identifier for maternal grandmother |
| m_mother_name    | TEXT         |                    | Name of maternal grandmother    |

**Foreign Keys:**
- `id` = `entry.horse_id`
- `id` = `history.horse_id`

---

### `history` Table
This table records historical race details for each horse, including their performance metrics.

| Column Name      | Data Type    | Key Type           | Description                     |
|------------------|--------------|--------------------|---------------------------------|
| id               | TEXT         | Primary Key        | Unique identifier for the history |
| horse_id         | TEXT         | Foreign Key        | Identifier for the horse        |
| race_date        | TEXT         |                    | Date of the race               |
| place            | TEXT         |                    | Location of the race           |
| round            | INTEGER      |                    | Round number                   |
| days             | INTEGER      |                    | Day of the racing event        |
| weather          | TEXT         |                    | Weather during the race        |
| race_number      | INTEGER      |                    | Number of the race             |
| race_id          | TEXT         | Foreign Key        | Identifier for the race         |
| race_name        | TEXT         |                    | Name of the race               |
| head_count       | INTEGER      |                    | Number of participating horses |
| bracket          | INTEGER      |                    | Bracket number                 |
| horse_number     | INTEGER      |                    | Horse number                   |
| win_odds         | REAL         |                    | Win odds of the horse          |
| popularity       | INTEGER      |                    | Popularity rank of the horse   |
| rank             | INTEGER      |                    | Final rank of the horse        |
| jockey_id        | TEXT         |                    | Identifier for the jockey       |
| jockey_name      | TEXT         |                    | Name of the jockey             |
| burden           | REAL         |                    | Weight burden carried by the horse |
| type             | TEXT         |                    | Type of the race               |
| length           | INTEGER      |                    | Distance of the race in meters |
| length_class     | TEXT         |                    | Classification by race length  |
| course           | TEXT         |                    | Type of course (e.g., turf)    |
| condition        | TEXT         |                    | Track condition                |
| rap_time         | REAL         |                    | Race time of the horse         |
| passage_rank     | TEXT         |                    | Passage rank during the race   |
| last_3f          | REAL         |                    | Time for the last 3 furlongs   |
| weight           | INTEGER      |                    | Horse weight during the race   |
| weight_diff      | INTEGER      |                    | Weight difference before the race |
| prize            | REAL         |                    | Prize money earned             |

**Foreign Keys:**
- `horse_id` = `horse.id`
- `race_id` = `race.id` (conditional: `race.race_date > history.race_date`)

---

### `result` Table
This table contains the final results of races, including the positions of each horse.

| Column Name      | Data Type    | Key Type           | Description                     |
|------------------|--------------|--------------------|---------------------------------|
| id               | TEXT         | Primary Key        | Unique identifier for the result |
| race_id          | TEXT         | Foreign Key        | Identifier for the race         |
| rank             | INTEGER      |                    | Final rank of the horse        |
| bracket          | INTEGER      |                    | Bracket number                 |
| horse_number     | INTEGER      |                    | Horse number                   |
| horse_id         | TEXT         |                    | Identifier for the horse        |
| horse_name       | TEXT         |                    | Name of the horse              |
| gender           | TEXT         |                    | Gender of the horse            |
| age              | INTEGER      |                    | Age of the horse               |
| burden           | REAL         |                    | Weight burden carried by the horse |
| jockey_id        | TEXT         |                    | Identifier for the jockey       |
| jockey_name      | TEXT         |                    | Name of the jockey             |
| rap_time         | REAL         |                    | Race time of the horse         |
| diff_time        | REAL         |                    | Time difference with the winner |
| passage_rank     | TEXT         |                    | Passage rank during the race   |
| last_3f          | REAL         |                    | Time for the last 3 furlongs   |
| weight           | INTEGER      |                    | Horse weight during the race   |
| weight_diff      | INTEGER      |                    | Weight difference before the race |
| trainer_id       | TEXT         |                    | Identifier for the trainer      |
| trainer_name     | TEXT         |                    | Name of the trainer            |
| prize            | REAL         |                    | Prize money earned             |

**Foreign Keys:**
- `race_id` = `race.id`
- `id` = `entry.id`
- `id` = `odds.id`

---

### `entry` Table
This table records entries of horses in races, including their assigned numbers and other details.

| Column Name      | Data Type    | Key Type           | Description                     |
|------------------|--------------|--------------------|---------------------------------|
| id               | TEXT         | Primary Key        | Unique identifier for the entry |
| race_id          | TEXT         | Foreign Key        | Identifier for the race         |
| bracket          | INTEGER      |                    | Bracket number                 |
| horse_number     | INTEGER      |                    | Horse number                   |
| horse_id         | TEXT         | Foreign Key        | Identifier for the horse        |
| horse_name       | TEXT         |                    | Name of the horse              |
| gender           | TEXT         |                    | Gender of the horse            |
| age              | INTEGER      |                    | Age of the horse               |
| burden           | REAL         |                    | Weight burden carried by the horse |
| jockey_id        | TEXT         |                    | Identifier for the jockey       |
| jockey_name      | TEXT         |                    | Name of the jockey             |
| trainer_id       | TEXT         |                    | Identifier for the trainer      |
| trainer_name     | TEXT         |                    | Name of the trainer            |
| weight           | INTEGER      |                    | Horse weight during the race   |
| weight_diff      | INTEGER      |                    | Weight difference before the race |

**Foreign Keys:**
- `race_id` = `race.id`
- `horse_id` = `horse.id`
- `horse_id` = `history.horse_id` (conditional: `race.race_date > history.race_date`)
- `id` = `result.id`
- `id` = `odds.id`

---

### `odds` Table
This table contains odds information for horses in races.

| Column Name      | Data Type    | Key Type           | Description                     |
|------------------|--------------|--------------------|---------------------------------|
| id               | TEXT         | Primary Key        | Unique identifier for the odds  |
| race_id          | TEXT         | Foreign Key        | Identifier for the race         |
| horse_number     | INTEGER      |                    | Horse number                   |
| win              | REAL         |                    | Win odds for the horse         |
| show_min         | REAL         |                    | Minimum show odds for the horse |
| show_max         | REAL         |                    | Maximum show odds for the horse |

**Foreign Keys:**
- `race_id` = `race.id`
- `id` = `entry.id`
- `id` = `result.id`
