from collections import defaultdict
import csv

# STEP 1: Build the group-to-max-city mapping
group_to_city_population = defaultdict(list)

with open("data_year_opening_lines.csv", "r", encoding="utf-8") as f, \
        open("data_year_opening_pop_lines.csv", "w", encoding="utf-8") as g:
    reader_1 = csv.reader(f)
    writer = csv.writer(g)
    for row in reader_1:
        if row[1] == "2406":
            writer.writerow(row)

with open("data_year_opening_pop_lines.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            year = row[3]
            city = row[6]
            line = row[18]
            pop = int(row[0])
            if year == "2021" and line:
                group_to_city_population[line].append((pop, city))
        except:
            continue

group_to_max_city = {
    group: max(city_list)[1] for group, city_list in group_to_city_population.items()
}

# STEP 2: Add max city to every row (overwrite cleanly)
with open("data_year_opening_pop_lines.csv", "r", encoding="utf-8") as f_in, \
     open("data_year_opening_pop_lines_final.csv", "w", encoding="utf-8", newline="") as f_out:

    reader = csv.reader(f_in)
    writer = csv.writer(f_out)

    header = next(reader)
    if "most_populous_city_1869" not in header:
        header.append("most_populous_city_1869")
    if "most_populous_city_2021" not in header:
        header.append("most_populous_city_2021")
    writer.writerow(header)

    for row in reader:
        group_id = row[18]
        most_populous = group_to_max_city.get(group_id, "")
        row.append(most_populous)
        row.append(most_populous)
        writer.writerow(row)


max_city_pop = {}
max_city_pop_2021 = {}
with open("data_year_opening_pop_lines_final.csv", "r", encoding="utf-8") as f_check:
    reader = csv.reader(f_check)
    header = next(reader)

    for row in reader:
        city = row[6]
        year = row[3]
        pop = row[0]
        if year == "1869" and city in group_to_max_city.values():
            max_city_pop[city] = pop
        elif year == "2021" and city in group_to_max_city.values():
            max_city_pop_2021[city] = pop



# STEP 3: Write final output (no duplication)
with open("data_year_opening_pop_lines_final.csv", "r", encoding="utf-8") as f_in, \
     open("final_pop_year_lines.csv", "w", encoding="utf-8", newline="") as f_out:

    reader = csv.reader(f_in)
    writer = csv.writer(f_out)

    next(reader)  # Skip header
    writer.writerow(
        ["obs_num", "pop", "year", "date", "municipal_code", "municipal", "orp_code", "orp",
         "county_code", "county", "region_code", "region", "rail_access", "rail_type",
         "opening_year", "cancelled", "oldest_line", "lines", "num_lines", "max_city_pop_1869", "max_city_pop_2021"]
    )

    for i, row in enumerate(reader, start=1):
        if r[1] == "2406":
            city = row[21]
            city_2021 = row[22]
            pop_1869 = max_city_pop.get(city, 0)
            pop_2021 = max_city_pop_2021.get(city_2021, 0)

            writer.writerow([
                i, row[0], row[3], row[4], row[5], row[6], row[7], row[8],
                row[9], row[10], row[11], row[12], row[14], row[15],
                row[16], row[17], row[18], row[19], row[20], pop_1869, pop_2021,
            ])
