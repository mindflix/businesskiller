import os, json


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Jobs:
    def __init__(self, level):
        self.level = level
        self.jobs_json = open("./jobs.json")

    def all_jobs(self):
        jobs = json.load(self.jobs_json)
        jobs = jobs.get("jobs")
        print(
            bcolors.BOLD
            + "{:<22} {:<10} {:<10}".format("Jobs", "Level", "Salary")
            + "\n-------------------------------------------"
            + bcolors.ENDC
        )
        for job in jobs:
            name = job.get("name")
            level = job.get("level")
            salary = job.get("salary")
            if level <= self.level:
                print(
                    bcolors.OKCYAN
                    + "{:<22} {:<10} {:<10}".format(name, level, str(salary) + "€")
                    + bcolors.ENDC
                )
            else:
                print(
                    bcolors.WARNING
                    + "{:<22} {:<10} {:<10}".format(name, level, str(salary) + "€")
                    + bcolors.ENDC
                )


class User:
    def __init__(self, username):
        self.username = username
        self.money = 0
        self.level = 0

    def __str__(self):
        return f"User -> {self.username}"

    def get_jobs(self):
        jobs = Jobs(self.level)
        jobs.all_jobs()


def create_user(username):
    check_save_json()
    user = {"id": get_last_id() + 1, "username": username}

    with open("./save.json", "r+") as file:
        obj = json.load(file)
        file.seek(0)
        obj["users"].append(user)
        json.dump(obj, file, indent=4)


def get_last_id():
    try:
        with open("./save.json", "r") as file:
            json_id = json.load(file)["users"][-1].get("id")
            return json_id
    except (IndexError):
        return -1


def check_save_json():
    model = {"users": [], "config": {}}

    file = open("./save.json", "r+")

    if is_json_exist():
        obj = json.load(file)
        missing = [key for key in model.keys() if key not in obj.keys()]
        file.seek(0)

        if len(missing) == True and "users" not in missing:
            for i in missing:
                obj[i] = {}
                json.dump(obj, file, indent=4)

        if len(missing) == True and "users" in missing:
            obj["users"] = []
            json.dump(obj, file, indent=4)
        file.close()
    else:
        json.dump(model, file, indent=4)
        file.close()
        check_save_json()


def is_json_exist():
    try:
        with open("./save.json", "r+") as file:
            json.load(file)
        return True
    except (json.JSONDecodeError):
        return False


def display_users():
    with open("./save.json", "r") as file:
        save = json.load(file)
        for user in save["users"]:
            print(
                bcolors.OKCYAN
                + str(user.get("id") + 1)
                + ". "
                + user.get("username")
                + bcolors.ENDC
            )


def main():
    while True:
        os.system("clear")
        request = input(
            bcolors.BOLD
            + "Welcome to BusiKiller Game\n"
            + "-------------------------------------------\n"
            + bcolors.WARNING
            + "1. Select or Create a user\n"
            + "2. Change configuration \n"
            + "3. Exit Busikiller \n"
            + "-> "
            + bcolors.ENDC
        )
        if request == "1":
            request = input(
                bcolors.BOLD
                + "\n-> Select or Create a user\n"
                + "-------------------------------------------\n"
                + bcolors.WARNING
                + "1. Create a new User\n"
                + "2. Select a User \n"
                + "-> "
                + bcolors.ENDC
            )
            if request == "1":
                username = input(
                    bcolors.BOLD
                    + "\n-> Username\n"
                    + "-------------------------------------------\n"
                    + bcolors.WARNING
                    + "-> "
                    + bcolors.ENDC
                )
                create_user(username)
            if request == "2":
                display_users()
                request = input(
                    bcolors.BOLD
                    + "\n-> Select a User\n"
                    + "-------------------------------------------\n"
                    + bcolors.WARNING
                    + "-> "
                    + bcolors.ENDC
                )

        if request == "3":
            exit()


if __name__ == "__main__":
    main()
