# Scheduler

📅 Welcome to the Scheduler application - your go-to tool for effortlessly generating schedules while managing unavailability and ensuring no double bookings occur on the same date.

## Features

- **Efficient Scheduling**: Generate schedules based on a task list, rules, and specified dates.
- **Unavailability Management**: Easily handle unavailability dates for individuals to ensure smooth scheduling.
- **Avoid Double Bookings**: Prevent double bookings on the same date and ensure fair distribution of tasks.

## Installation

1. Clone the repository: `git clone https://github.com/your-username/scheduler.git`
2. Install the required packages: `pip install -r requirements.txt`

## Usage

1. Edit the `tasklist.json` file to define the tasks and their assigned people.
2. Edit the `days.json` file to define the days to schedule.
3. Edit the `unavailability.json` file to define the unavailability dates.
4. Run the `scheduler.py` script: `python scheduler.py`
5. The generated schedule will be printed to the console and saved as a CSV file.

## Schedule Structure

The generated schedule is a list of dictionaries, where each dictionary represents a schedule for a single date. Each schedule contains the following keys:

- `date`: The date of the schedule.
- `tasks`: A list of dictionaries, where each dictionary represents a task and its assigned people. Each task contains the following keys:
  - `role`: The role of the task.
  - `assigned`: A list of dictionaries, where each dictionary represents a person assigned to the task. Each person contains the following keys:
    - `name`: The name of the person.

## Contributing

👍 Contributions are welcome! If you find any issues or have any suggestions, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.