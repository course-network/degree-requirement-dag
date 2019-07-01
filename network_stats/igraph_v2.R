
library(dplyr)
library(igraph)


reqs <- read.csv("./parse_course_requirements/edges.csv", header = F)
# reqs <- read.csv("../Pickle to CSV/6-30/edges.csv", header = F)
#  Using this file locally until we merge branches.


head(reqs)
names(reqs) <- c("pre_rec", "course")


req_net <- graph_from_data_frame(reqs, directed = T)
plot(req_net, directed = T)
tree_layout <- layout.reingold.tilford(req_net, root = "ST 623", circular = FALSE, flip.y = FALSE)


# stat <- stat %>% select(ref, course, pre_rec, name)
# names(reqs) <- c("course", "ref", "pre_rec", "name")
# stat <- stat %>% select(ref, course, pre_rec, name)
# st_net <- graph_from_data_frame(stat, directed = T)
# plot(st_net)

st_net <- graph_from_data_frame(stat, directed = T)
plot(st_net)
plot(st_net, edge.color = stat$pre_rec, edge.curved = 0.3, edge.width = 2) # Thicker lines

# Calculate node degree
degree(st_net)
plot(st_net, vertex.color = degree(st_net))





# Counting dependencies ------------------------------

# Pre requisite department (academic unit)
reqs$pre_dept <- sub(x = reqs$pre_rec, 
                     pattern = "([A-z]+) .+", 
                     replacement = "\\1")

# Course department (academic unit)
reqs$course_dept <- sub(x = reqs$course, 
                     pattern = "([A-z]+) .+", 
                     replacement = "\\1")

# There are about half of pre-requisites that
#  were in-department.
table(reqs$pre_dept == reqs$course_dept)

reqs$pre_dept[reqs$pre_dept == "NE"] <- "NSE"
# Count number of dependencies.
reqs %>% filter(pre_dept != "of") %>%
  group_by(pre_dept) %>% 
  summarise(n = n()) %>% arrange(desc(n))

# Count number of 
# Nuclear science got changed to NSE.
reqs$pre_dept[reqs$pre_dept == "NE"] <- "NSE"
reqs %>% filter(pre_dept != "and", pre_dept != "or", pre_dept != "of", pre_dept != course_dept) %>%
  group_by(pre_dept) %>% 
  summarise(n = n()) %>% arrange(desc(n))


# This is going to require some trickery to pass the OR nodes through as pre-requisites.
#  Maybe they shoudn't count at full weight if they're an OR?  
#  Count it proportional to the number of elements in the OR maybe?


# Create a small plot, math meets CS ------------------------------
# This will require the OR node data.






