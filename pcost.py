def portfolio_cost(filename) -> float:
    total_cost = 0
    with open(filename, "r") as data:
        for line in data.readlines():
            try:
                total_cost += int(line.split()[1]) * float(line.split()[2])
            except ValueError as e:
                print("Couldn't covert the attributes to int/float")
                print(f"Error: {e}")
    return total_cost

if __name__=="__main__":

    print(portfolio_cost("../Data/portfolio3.dat"))