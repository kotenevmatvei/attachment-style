import csv
import tabulate

correct_csv_names = [
    "correct_scores_before_revert.csv",
    "correct_scores_after_revert.csv",
    "correct_averages.csv",
]

app_csvs_names = [
    "app_scores_before_revert.csv",
    "app_scores_after_revert.csv",
    "app_averages.csv",
]

headers = ["file", "case_ind", "element_ind", "correct_element", "app_element"]
discrepancies = []
num_of_correct_cases = 0
for correct_csv_name, app_csv_name in zip(correct_csv_names, app_csvs_names):
    correct_data = []
    with open(correct_csv_name, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            correct_data.append(row)

    app_data = []
    with open(app_csv_name, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            app_data.append(row)

    if len(app_data) == len(correct_data):
        num_cases = len(app_data)
        print("Number of Cases: ", num_cases)
    else:
        raise ValueError("Different numbers of cases!")

    for case_ind in range(num_cases):
        correct_row = correct_data[case_ind]
        app_row = app_data[case_ind]
        case_discrepancies = []

        if len(correct_row) == len(app_row):
            num_elements = len(correct_row)
        else:
            raise ValueError(f"Different numbers of scores in case {case_ind}")

        for element_ind in range(num_elements):
            correct_element = correct_data[case_ind][element_ind]
            app_element = app_data[case_ind][element_ind]
            if correct_element != app_element:
                file = "".join(app_csv_name.split("_")[1:])
                case_discrepancies.append(
                    [file, case_ind, element_ind, correct_element, app_element]
                )

        if not case_discrepancies:
            num_of_correct_cases += 1

    discrepancies += case_discrepancies


print("Number of correct cases: ", num_of_correct_cases)
print("Table with discrepancies:")
print(tabulate.tabulate(discrepancies, headers, tablefmt="orgtbl"))
