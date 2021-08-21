# cs_subset.R ------------------------------
#' 
#' Create a subset of courses to work on for CS.
#'  Includes all courses in CS, plus all courses and OR nodes which
#'  are pre-requisites for CS.
#'
# ....................................



library(dplyr)
library(igraph)


reqs <- read.csv("./course_data/csv/courses_parsed_edges.csv", header = F)
node <- read.csv("./course_data/csv/courses_parsed_nodes.csv", header = F)

names(reqs) <- c("pre_req", "course")
names(node) <- c("course", "order")

# Identify Academic Units.
# Pre requisite department (academic unit)
reqs$pre_dept <- sub(x = reqs$pre_req,
                     pattern = "([A-z]+) .+",
                     replacement = "\\1")

# Course department (academic unit)
reqs$course_dept <- sub(x = reqs$course,
                        pattern = "([A-z]+) .+",
                        replacement = "\\1")

# reqs$pre_dept[reqs$pre_dept == "NE"] <- "NSE"
reqs <- reqs %>% filter(pre_dept != "NE")



# Try to get CS only.
head(reqs)
head(node)

# 20 items in CS requires something as an OR. 
or_to_cs <- reqs %>% filter(course_dept == "CS" & pre_dept == "OR")
# 27 courses lead into a CS OR.
input_to_cs_or <- reqs %>% filter(course %in% or_to_cs$pre_req)
# 16 courses lead into CS which are not an OR.
input_to_cs <- reqs %>% filter(course_dept == "CS" & !(pre_dept %in% c("OR", "CS")))
# 68 courses lead from CS to CS
cs_to_cs <- reqs %>% filter(course_dept == "CS" & pre_dept == "CS")
# Combine and filter
cs <- rbind(or_to_cs, 
            input_to_cs_or,
            input_to_cs,
            cs_to_cs) %>% distinct()

<<<<<<< HEAD
# Identify CS Nodes
cs_node <- node %>% filter(course %in% c(as.character(cs$pre_req), 
                                         as.character(cs$course)))

# Write Edges and Nodes to disk
write.csv(file = "./course_data/csv/CS/CS_edge.csv", x = cs, row.names = F)
write.csv(file = "./course_data/csv/CS/CS_node.csv", x = cs_node, row.names = F)
=======
>>>>>>> 40b4a8d9c75c87e69c56cdf3d15abf80ee595c81

