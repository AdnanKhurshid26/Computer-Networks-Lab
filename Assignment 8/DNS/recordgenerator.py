from faker import Faker

infile = open("domainnames.txt", "r")
outfile = open("records.txt", "w")

while True:
    line = infile.readline()
    if not line:
        break
    line =  line[:-1] + "," + Faker().ipv4() + "\n"
    outfile.write(line)

    
