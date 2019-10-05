# layout_order.R ------------------------------
#' Issue 10:
#' 
#' The topological order could be used for determining the node level (y-axis coordinate) in the 
#' tree-version graph. This issue is to implement a script to take raw courses data and generate 
#' the topological orders for them.
#' 
#' 
# ....................................


library(igraph)
?igraph
library(dplyr)

# Read data
reqs   <- read.csv("./course_data/csv/courses_parsed_edges.csv", header = F)
course <- read.csv("./course_data/csv/courses_parsed_nodes.csv", header = F)



names(reqs) <- c("pre_rec", "course")
names(course) <- c("course", "n")

# This will require the OR node data.
reqs$pre_dept <- sub(x = reqs$pre_rec,
                     pattern = "([A-z]+) .+",
                     replacement = "\\1")

# Course department (academic unit)
reqs$course_dept <- sub(x = reqs$course,
                        pattern = "([A-z]+) .+",
                        replacement = "\\1")


# Course department (academic unit)
course$course_dept <- sub(x = course$course,
                        pattern = "([A-z]+) .+",
                        replacement = "\\1")


# Set seed nodes
# Find degree:
head(reqs)
head(course)
course %>% filter(course_dept == "OR") %>% arrange(desc(n))
reqs %>% filter(course == "OR 66")
reqs %>% filter(pre_rec == "OR 66")
# the course ATS 310 has one pre-requisite that can be filled by any of 7 courses.
#  (It has some other pre-requisites also.)

cs <- course %>% filter(course_dept == "CS")
join_cs <- left_join(cs %>% select(-n), 
                     reqs, by = c("course"))
head(join_cs)
sum(is.na(join_cs$pre_rec))
join_cs %>% filter(is.na(pre_rec))


# What we really want is a CS course with no PR in CS, so lets find all the courses with CS PR.
cs_only <- left_join(cs %>% select(-n), 
                       reqs %>% filter((course_dept == "CS") & (pre_dept == "CS")), by = c("course"))

cs_only %>% arrange(course)
cs_only %>% filter(is.na(pre_rec)) %>% select(course)
# These courses have no pre-req in CS.

# CS Courses with PR in CS, by PR.
# These are direct PRs only, don't include the OR group.
cs_only %>% filter(!is.na(pre_rec)) %>% 
  group_by(pre_rec) %>% summarise(n = n()) %>% data.frame()

# If we include the OR group then we get,
csor <- course %>% filter(course_dept %in% c("CS", "OR"))
csor_join <- left_join(csor %>% select(-n), 
                  reqs %>% filter((course_dept %in% c("CS", "OR")) & 
                                    (pre_dept == "CS")),
                  by = c("course"))
csor_join %>% filter(!is.na(pre_rec)) %>% 
  group_by(pre_rec) %>% summarise(n = n()) %>% data.frame()

# These are courses which nothing else uses.
csor_join %>% filter(!is.na(pre_rec)) %>% 
  group_by(pre_rec) %>% summarise(n = n()) %>% data.frame() %>% 
  filter(n == 1)


# These are CS courses which have no pre-reqs.
seed_group <- csor_join %>% filter(is.na(pre_rec)) %>% arrange(course) %>% 
  filter(course_dept.x == "CS") %>% select(course)
seed_group$rank <- sub(x = seed_group$course, pattern = ".+ ([0-9])[0-9]+", replacement = "\\1")
sub(x = seed_group$course, pattern = ".+ ([0-9])[0-9]+", replacement = "\\1")


seed_group
seed_group %>% filter(rank == 1)


csor_list <- reqs %>% filter(course_dept == "CS" & pre_dept == "OR") %>%
  select(pre_rec) %>% distinct() %>% unlist() %>% as.vector()
csor_edges <- reqs %>% filter(pre_rec %in% csor_list | course %in% csor_list)

# Now we want all the edges that feed into a CS course.
cs_edges <- reqs %>% filter(course_dept == "CS")

# Append these two edge lists.
full_cs_edges <- rbind(cs_edges, csor_edges) %>% distinct()
dim(full_cs_edges)
dim(csor_edges)
dim(cs_edges)
# 20 overlap, which is good.

edge_matrix <- as.matrix(full_cs_edges[ , c("pre_rec", "course")])
csnet <- graph_from_edgelist(el = edge_matrix, directed = T)
plot(csnet)

# So if this is the right set of edges, 
#  Find all adjacent ones to the starting set.
rank1 <- seed_group %>% filter(rank == 1) %>% select(course) %>% unlist() %>% as.vector()
adj_rank1 <- adjacent_vertices(graph = csnet, v = rank1)
adj_rank1[[1]]
adj_rank1[[2]]
adj_rank1[[3]]
adj_rank1[[4]]

# Looking around a little bit...
reqs %>% filter(course == "CS 395")
reqs %>% filter(course == "OR 438")
reqs %>% filter(course == "OR 428")
# OK yes, this CS course really can have an OR requirement with ART 120.
#  However, ART 120 doesn't exist anymore.
#  The course is a website design course. 

find_adjacent <- function(){
  
}




# Could the same thing be had by filtering reqs?
# Not quickly because you have to do some joining I think.  It requires pre-req to be CS, 
#  the course should be a CS course or an OR node, but only if that OR node leads to a CS course.
head(reqs)
# CS courses  which have pre-reqs, in any department?
# reqs %>% group_by(pre_rec) %>% filter(pre_dept == "CS", course_dept %in% c("OR", "CS")) %>% summarise(n = n())

# What we really want is a CS course with no PR in CS.
join_nocs <- left_join(cs %>% select(-n), 
                     reqs %>% filter(!(course_dept == "CS") & !(pre_dept == "OR")), by = c("course"))



# We really need to know if an OR node contains a CS course.

reqs %>% filter(course == "CS 261")
reqs %>% filter(course == "OR 428")

head(join_nocs)
join_nocs %>% arrange(course)

nocs2 <- reqs %>% filter(!(course_dept == "CS") & !(pre_dept == "OR"))


# For each in seed set, 


#    Find all adjacent nodes

# 




